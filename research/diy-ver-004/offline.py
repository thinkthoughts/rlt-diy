"""Offline byte-integrity verifier for DIY-VER-003 v1; no release authority."""
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path

# Fixed profile, independent of the package manifest and commitment.
NAMES = (
    "methodology/DIY-VER-001.md",
    "specifications/DIY-D1-001.md", "specifications/DIY-S1-001.md",
    "evidence/register.json", "evidence/register.schema.json",
    "evidence/s1-vps-001.json",
    "d1/README.md", "d1/verify.py", "d1/test_verify.py",
    "d1/batch.json", "d1/fixture.json",
    "s1/README.md", "s1/verify.py", "s1/test_verify.py", "s1/fixture.json",
    "ver/README.md", "ver/verify.py", "ver/test_verify.py", "manifest.json",
)
LIMIT = 2_000_000
PROFILE = "DIY-VER-003-v1"

class Rejected(ValueError):
    pass

def require(ok, message):
    if not ok:
        raise Rejected(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def ishash(x):
    return type(x) is str and re.fullmatch("[0-9a-f]{64}", x) is not None

def pairs(items):
    out = {}
    for k, v in items:
        require(k not in out, "duplicate JSON key")
        out[k] = v
    return out

def parse(data):
    return json.loads(data.decode("utf-8"), object_pairs_hook=pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(Rejected("nonfinite number")))

def obj(x, keys):
    require(type(x) is dict and set(x) == set(keys), "object schema")
    return x

def regular(path):
    require(stat.S_ISREG(path.lstat().st_mode), "nonregular file")
    with path.open("rb") as f:
        data = f.read(LIMIT + 1)
    require(len(data) <= LIMIT, "size limit")
    return data

def inventory(root):
    require(stat.S_ISDIR(root.lstat().st_mode), "nonregular root")
    files, dirs = set(), set()
    def onerror(e):
        raise e
    for parent, names, items in os.walk(root, followlinks=False, onerror=onerror):
        for n in names:
            p = Path(parent) / n
            require(stat.S_ISDIR(p.lstat().st_mode), "nonregular directory")
            dirs.add(p.relative_to(root).as_posix())
        for n in items:
            p = Path(parent) / n
            require(stat.S_ISREG(p.lstat().st_mode), "nonregular file")
            files.add(p.relative_to(root).as_posix())
    expected_dirs = {p.as_posix() for n in NAMES for p in Path(n).parents if p != Path(".")}
    require(files == set(NAMES) and dirs == expected_dirs, "inventory mismatch")

def snapshot(root):
    inventory(root)
    return {name: regular(root / name) for name in NAMES}

def check_manifest(data):
    m = obj(parse(data["manifest.json"]), ("schema_version", "profile", "acceptance", "files"))
    require(type(m["schema_version"]) is int and m["schema_version"] == 1 and
            m["profile"] == PROFILE and m["acceptance"] == "PENDING", "package metadata")
    obj(m["files"], set(NAMES) - {"manifest.json"})
    for name, item in m["files"].items():
        obj(item, ("commit", "source", "bytes", "sha256"))
        require(type(item["commit"]) is str and re.fullmatch("[0-9a-f]{40}", item["commit"]),
                "commit syntax")
        require(type(item["source"]) is str and item["source"], "source locator")
        require(type(item["bytes"]) is int and item["bytes"] == len(data[name]) and
                ishash(item["sha256"]) and item["sha256"] == digest(data[name]),
                "manifest payload mismatch")

def envelope(data):
    check_manifest(data)
    return {"schema_version": 1, "profile": PROFILE,
            "purpose": "BYTE_INTEGRITY_ONLY", "acceptance": "PENDING",
            "files": {name: {"bytes":len(value), "sha256":digest(value)}
                      for name, value in sorted(data.items())}}

def encode(x):
    return (json.dumps(x, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode("utf-8")

def issue(root, output):
    # Issuer must independently establish provenance before trusting this snapshot.
    raw = encode(envelope(snapshot(root)))
    require(not output.is_symlink(), "commitment symlink")
    require(root.resolve() not in (output.resolve(), *output.resolve().parents),
            "commitment must be outside package")
    with output.open("xb") as f:
        f.write(raw)
    return {"status":"COMMITMENT_CREATED_UNAUTHENTICATED", "anchor_sha256":digest(raw),
            "files":len(NAMES), "acceptance":"PENDING"}

def verify(root, commitment, anchor):
    require(ishash(anchor), "external anchor must be 64 lowercase hex characters")
    raw = regular(commitment)
    require(digest(raw) == anchor, "external anchor mismatch")
    got = parse(raw)
    data = snapshot(root)
    require(encode(got) == encode(envelope(data)), "anchored artifact mismatch")
    return {"status":"OFFLINE_INTEGRITY_MATCH", "files":len(NAMES),
            "anchor_sha256":anchor, "acceptance":"PENDING",
            "source_provenance_verified":False, "issuer_authenticated":False,
            "checker_execution_verified":False, "release_authority":False}

def main(argv):
    try:
        if len(argv) == 4 and argv[1] == "issue":
            result = issue(Path(argv[2]).absolute(), Path(argv[3]).absolute())
        elif len(argv) == 5 and argv[1] == "verify":
            result = verify(Path(argv[2]).absolute(), Path(argv[3]).absolute(), argv[4])
        else:
            print("usage: offline.py issue PACKAGE COMMITMENT | verify PACKAGE COMMITMENT TRUSTED_SHA256",
                  file=sys.stderr)
            return 2
        print(json.dumps(result, sort_keys=True))
    except (ValueError, OSError, RecursionError, TypeError, KeyError) as e:
        print("REJECT: " + str(e), file=sys.stderr)
        return 1
    return 2  # No release approval path.

if __name__ == "__main__":
    sys.exit(main(sys.argv))
