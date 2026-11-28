"""DIY-VER-002: frozen pending-register validator, not a release authority."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "6cf606def424a512efae27af460a9cf89f4cda9b"
PREFIX = "research/diy-ver-001/"
REGISTER = PREFIX + "register.json"
SCHEMA = PREFIX + "register.schema.json"
EVIDENCE = PREFIX + "evidence/s1-vps-001.json"
PATHS = (REGISTER, SCHEMA, EVIDENCE)
S1 = "5099cf7cabb073fb6fb60a2e086f78087aa366f7"
D1 = "8c1eff6df4dcdec7007449e6b8704de12b4d9f66"
SPEC = "eddc9ebd7d1e712cf0a0a01c8e3a45b37762f8d7"
AXES = ("statement_identity", "source_fidelity", "analytical_proof",
        "lean_check", "rlt_check", "software_execution",
        "implementation_correspondence", "external_observation",
        "physical_validation", "independent_review")

class Rejected(ValueError):
    pass

def require(ok, msg):
    if not ok:
        raise Rejected(msg)

def obj(x, keys):
    require(type(x) is dict and set(x) == set(keys), "schema mismatch")
    return x

def pairs(items):
    out = {}
    for k, v in items:
        require(k not in out, "duplicate JSON key")
        out[k] = v
    return out

def parse(data):
    require(len(data) <= 2_000_000, "size limit")
    return json.loads(data.decode("utf-8"), object_pairs_hook=pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(Rejected("nonfinite number")))

def git(root, *args):
    env = dict(__import__("os").environ)
    for k in list(env):
        if k.startswith("GIT_"):
            del env[k]
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    return subprocess.run(["git", "--no-replace-objects", "-C", str(root), *args],
                          check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=env, timeout=30).stdout

def frozen(root, path):
    # Compare exact tracked blob bytes from the pinned baseline.
    require(path in PATHS, "unregistered artifact path")
    expected = git(root, "show", BASE + ":" + path)
    p = root
    for part in path.split("/"):
        p = p / part
        require(not p.is_symlink(), "symlink refused")
    require(p.is_file(), "missing artifact")
    with p.open("rb") as f:
        current = f.read(2_000_001)
    require(current == expected, "artifact differs from frozen baseline: " + path)
    return current

def check_records(r, e):
    obj(r, ("schema_version", "records"))
    require(type(r["schema_version"]) is int and r["schema_version"] == 1, "schema version")
    require(type(r["records"]) is list and len(r["records"]) == 2, "record inventory")
    seen = set()
    for row in r["records"]:
        obj(row, ("id", "scope", "specification", "candidate", "axes", "acceptance", "open_obligations"))
        name = row["id"]
        require(type(name) is str and name in ("DIY-D1-002", "DIY-S1-002") and name not in seen,
                "record identity")
        seen.add(name)
        is_s1 = name == "DIY-S1-002"
        stem = "s1" if is_s1 else "d1"
        pin = S1 if is_s1 else D1
        specpath = ("foundations/clean-datacenters/DIY-S1-001.md" if is_s1 else
                    "foundations/clean-money-systems/DIY-D1-001.md")
        require(row["specification"] == {"commit": SPEC, "path": specpath}, "specification identity")
        require(row["candidate"] == {"repository": "https://github.com/thinkthoughts/rlt-diy",
                "commit": pin, "path": "research/diy-" + stem + "-002/"}, "candidate identity")
        require(type(row["scope"]) is str and bool(row["scope"].strip()), "scope")
        obligations = row["open_obligations"]
        require(type(obligations) is list and len(obligations) == 4 and
                all(type(x) is str and x.strip() for x in obligations) and
                len(set(obligations)) == len(obligations), "open obligations")
        require(row["acceptance"] == {"decision": "PENDING", "reviewer": None,
                "review_record": None}, "release authorization unavailable")
        obj(row["axes"], AXES)
        for axis, item in row["axes"].items():
            obj(item, ("status", "evidence", "scope"))
            reported = is_s1 and axis == "software_execution"
            require(item["status"] == ("REPORTED_PASS" if reported else "PENDING"),
                    "unauthorized status change")
            require(item["evidence"] == (["evidence/s1-vps-001.json"] if reported else []),
                    "evidence reference mismatch")
            require(type(item["scope"]) is str and bool(item["scope"].strip()), "axis scope")
    require(seen == {"DIY-D1-002", "DIY-S1-002"}, "incomplete inventory")
    obj(e, ("schema_version", "record_id", "kind", "date", "candidate_reference",
            "observed_checkout", "environment", "commands", "tests", "gate_exit",
            "result", "limitations"))
    require(type(e["schema_version"]) is int and e["schema_version"] == 1, "evidence schema version")
    require(e["record_id"] == "DIY-S1-002-VPS-001" and
            e["kind"] == "operator_reported_execution" and
            e["candidate_reference"] == S1 and e["observed_checkout"] is None,
            "evidence identity/scope")
    tests = obj(e["tests"], ("run", "failures", "errors", "elapsed_seconds"))
    require(all(type(tests[k]) is int for k in ("run", "failures", "errors")) and
            (tests["run"], tests["failures"], tests["errors"]) == (12, 0, 0),
            "test counts")
    require(type(e["gate_exit"]) is int and e["gate_exit"] == 2, "gate exit")
    result = e["result"]
    require(type(result) is dict and result.get("status") == "SYNTHETIC_ACCOUNTING" and
            result.get("acceptance") == "PENDING" and result.get("physical_validation") is False and
            result.get("comparability_verified") is False, "evidence acceptance boundary")

def verify(root):
    raw = {p: frozen(root, p) for p in PATHS}
    check_records(parse(raw[REGISTER]), parse(raw[EVIDENCE]))
    # Schema is byte-pinned, not executed as a general JSON Schema validator.
    parse(raw[SCHEMA])
    return {"status": "FROZEN_INVENTORY_MATCH", "records": 2, "axes": 20,
            "reported_pass": 1, "pending_axes": 19, "acceptance": "PENDING",
            "independent_review": False, "release_authority": False,
            "candidate_execution_verified": False,
            "baseline": BASE, "sha256": {p: hashlib.sha256(b).hexdigest() for p, b in raw.items()}}

def main(argv):
    if len(argv) != 2:
        print("usage: python3 verify.py REPOSITORY_ROOT", file=sys.stderr)
        return 2
    try:
        print(json.dumps(verify(Path(argv[1]).resolve()), sort_keys=True))
    except (ValueError, OSError, subprocess.SubprocessError, RecursionError, TypeError, KeyError) as e:
        print("REJECT: " + str(e), file=sys.stderr)
        return 1
    return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv))
