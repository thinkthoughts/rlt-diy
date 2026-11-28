"""Synthetic distribution arithmetic/attribution checker. No signature or chain verification."""
import json
import sys
from pathlib import Path

class Rejected(ValueError):
    pass

def require(ok, message):
    if not ok:
        raise Rejected(message)

def obj(x, keys):
    require(type(x) is dict and set(x) == set(keys.split()), "object schema")
    return x

def ident(x):
    require(type(x) is str and 0 < len(x) <= 128 and x.isascii()
            and all(c.isalnum() or c in "-_:" for c in x), "identifier")
    return x

def nat(x):
    require(type(x) is int and 0 <= x <= 2**63-1, "integer range/type")
    return x

def seq(x):
    require(type(x) is list and len(x) <= 10000, "list schema/limit")
    return x

def unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, "duplicate JSON key")
        out[key] = value
    return out

def load(path):
    with open(path, "rb") as f:
        data = f.read(2_000_001)
    require(len(data) <= 2_000_000, "file size limit")
    return json.loads(data.decode("utf-8"), object_pairs_hook=unique_pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(Rejected("nonfinite number")))

def verify(batch, fixture):
    obj(batch, "schema batch_id network asset rule_id rows")
    obj(fixture, "schema network asset batch_id rule contributions outputs")
    require(batch["schema"] == "diy-d1-synthetic-v1" and
            fixture["schema"] == "diy-d1-fixture-v1", "schema version")
    for k in ("network", "asset", "batch_id"):
        require(ident(batch[k]) == ident(fixture[k]), "context mismatch")
    require(batch["network"] == "synthetic", "synthetic network only")
    rule = obj(fixture["rule"], "id numerator denominator")
    require(ident(batch["rule_id"]) == ident(rule["id"]), "rule mismatch")
    n, d = nat(rule["numerator"]), nat(rule["denominator"])
    require(d > 0, "zero denominator")
    contributions = {}
    for c in seq(fixture["contributions"]):
        obj(c, "id participant units destination")
        key = ident(c["id"])
        require(key not in contributions, "duplicate fixture contribution")
        contributions[key] = (ident(c["participant"]), nat(c["units"]), ident(c["destination"]))
    outputs = {}
    for o in seq(fixture["outputs"]):
        obj(o, "txid vout destination amount")
        key = (ident(o["txid"]), nat(o["vout"]))
        require(key not in outputs, "duplicate fixture output")
        outputs[key] = (ident(o["destination"]), nat(o["amount"]))
    seen, allocation = set(), {}
    total = 0
    for row in seq(batch["rows"]):
        obj(row, "contribution_id participant units destination amount txid vout")
        cid = ident(row["contribution_id"])
        require(cid in contributions and cid not in seen, "unknown/duplicate contribution")
        seen.add(cid)
        p, u, dest = contributions[cid]
        require((ident(row["participant"]), nat(row["units"]), ident(row["destination"]))
                == (p, u, dest), "contribution mismatch")
        expected = nat(u * n // d)
        amount = nat(row["amount"])
        require(amount == expected, "payment arithmetic mismatch")
        key = (ident(row["txid"]), nat(row["vout"]))
        require(key in outputs and outputs[key][0] == dest, "output attribution mismatch")
        allocation[key] = nat(allocation.get(key, 0) + amount)
        total = nat(total + amount)
    require(seen == set(contributions), "incomplete contribution set")
    require(set(allocation) == set(outputs), "unmatched output")
    for key, amount in allocation.items():
        require(amount == outputs[key][1], "output allocation mismatch")
    return {"status": "SYNTHETIC_MATCH", "rows": len(seen), "outputs": len(outputs),
            "total_base_units": total, "acceptance": "PENDING",
            "signature_verified": False, "chain_verified": False}

def main(argv):
    if len(argv) != 3:
        print("usage: python3 verify.py BATCH FIXTURE", file=sys.stderr)
        return 2
    try:
        print(json.dumps(verify(load(argv[1]), load(argv[2])), sort_keys=True))
    except (ValueError, OSError, UnicodeError, RecursionError) as e:
        print("REJECT: " + str(e), file=sys.stderr)
        return 1
    return 2  # synthetic match is not full acceptance

if __name__ == "__main__":
    sys.exit(main(sys.argv))
