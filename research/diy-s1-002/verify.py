"""Bounded synthetic resource-accounting model, not physical validation."""
import json
import re
import sys
from fractions import Fraction

class Rejected(ValueError):
    pass

def require(ok, msg):
    if not ok:
        raise Rejected(msg)

def obj(x, keys):
    require(type(x) is dict and set(x) == set(keys.split()), "object schema")
    return x

def ident(x):
    require(type(x) is str and re.fullmatch(r"[A-Za-z0-9_:-]{1,128}", x)
            is not None, "identifier")
    return x

def q(x):
    require(type(x) is str and re.fullmatch(r"(0|[1-9][0-9]{0,11})(\.[0-9]{1,9})?", x)
            is not None, "nonnegative decimal string required")
    return Fraction(x)

def bounds(x):
    require(type(x) is list and len(x) == 2, "interval schema")
    lo, hi = map(q, x)
    require(lo <= hi, "inverted bounds")
    return lo, hi

def add(a, b):
    return a[0] + b[0], a[1] + b[1]

def mul(a, b):
    return a[0] * b[0], a[1] * b[1]

def div(a, b):
    require(b[0] > 0, "positive lower work bound required")
    return a[0] / b[1], a[1] / b[0]

def serial(a):
    return [str(x) for x in a]

def pairs(items):
    out = {}
    for k, v in items:
        require(k not in out, "duplicate JSON key")
        out[k] = v
    return out

def load(path):
    with open(path, "rb") as f:
        data = f.read(2_000_001)
    require(len(data) <= 2_000_000, "file size limit")
    return json.loads(data.decode("utf-8"), object_pairs_hook=pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(Rejected("nonfinite number")))

def run(x):
    obj(x, "id hardware software meter intensity_source embodied_source work intervals embodied_gco2e")
    for k in ("id", "hardware", "software", "meter", "intensity_source", "embodied_source"):
        ident(x[k])
    work = bounds(x["work"])
    require(work[0] > 0, "positive lower work bound required")
    intervals = x["intervals"]
    require(type(intervals) is list and 0 < len(intervals) <= 1000, "interval list")
    energy = operational = (Fraction(0), Fraction(0))
    last = 0
    for row in intervals:
        obj(row, "start_s end_s energy_kwh intensity_gco2e_per_kwh")
        a, b = row["start_s"], row["end_s"]
        require(type(a) is int and type(b) is int and a == last and a < b <= 10**9,
                "interval gap, overlap or invalid time")
        last = b
        e, i = bounds(row["energy_kwh"]), bounds(row["intensity_gco2e_per_kwh"])
        energy = add(energy, e)
        operational = add(operational, mul(e, i))
    embodied = bounds(x["embodied_gco2e"])
    return {"energy_kwh": energy, "operational_gco2e": operational,
            "embodied_gco2e": embodied, "total_gco2e": add(operational, embodied),
            "energy_per_work": div(energy, work),
            "emissions_per_work": div(add(operational, embodied), work)}

def relation(candidate, baseline):
    if candidate[1] < baseline[0]:
        return "STRICTLY_LOWER"
    if candidate[0] > baseline[1]:
        return "STRICTLY_HIGHER"
    return "NOT_RESOLVED_BY_BOUNDS"

def verify(x):
    obj(x, "schema context baseline candidate")
    require(x["schema"] == "diy-s1-synthetic-v1", "synthetic schema only")
    ctx = obj(x["context"], "workload quality functional_unit boundary region period")
    for k in ctx:
        ident(ctx[k])
    # Both runs share these declared labels; equivalence is assumed, not measured.
    require(x["baseline"]["id"] != x["candidate"]["id"], "distinct run identifiers")
    b, c = run(x["baseline"]), run(x["candidate"])
    return {"status": "SYNTHETIC_ACCOUNTING", "acceptance": "PENDING",
            "physical_validation": False, "comparability_verified": False,
            "baseline": {k: serial(v) for k, v in b.items()},
            "candidate": {k: serial(v) for k, v in c.items()},
            "comparison": {k: relation(c[k], b[k]) for k in
                           ("energy_per_work", "emissions_per_work")}}

def main(argv):
    if len(argv) != 2:
        print("usage: python3 verify.py FIXTURE", file=sys.stderr)
        return 2
    try:
        print(json.dumps(verify(load(argv[1])), sort_keys=True))
    except (ValueError, OSError, UnicodeError, RecursionError, KeyError, TypeError) as e:
        print("REJECT: " + str(e), file=sys.stderr)
        return 1
    return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv))
