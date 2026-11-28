"""Build/check a fixed-profile portable research directory. No release authority."""
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

VER = "14541fdc1377c31982d96d7f226a101b1fa25ba9"
D1 = "8c1eff6df4dcdec7007449e6b8704de12b4d9f66"
S1 = "5099cf7cabb073fb6fb60a2e086f78087aa366f7"
# Independent profile: not read from a package or its manifest.
PROFILE = {
    "methodology/DIY-VER-001.md": (VER, "methodology/DIY-VER-001.md"),
    "specifications/DIY-D1-001.md": (VER, "foundations/clean-money-systems/DIY-D1-001.md"),
    "specifications/DIY-S1-001.md": (VER, "foundations/clean-datacenters/DIY-S1-001.md"),
    "evidence/register.json": (VER, "research/diy-ver-001/register.json"),
    "evidence/register.schema.json": (VER, "research/diy-ver-001/register.schema.json"),
    "evidence/s1-vps-001.json": (VER, "research/diy-ver-001/evidence/s1-vps-001.json"),
}
for prefix, pin, names in (
    ("d1", D1, ("README.md", "verify.py", "test_verify.py", "batch.json", "fixture.json")),
    ("s1", S1, ("README.md", "verify.py", "test_verify.py", "fixture.json")),
    ("ver", VER, ("README.md", "verify.py", "test_verify.py")),
):
    for name in names:
        PROFILE[prefix + "/" + name] = (pin, "research/diy-" + prefix + "-002/" + name)
MANIFEST = "manifest.json"
LIMIT = 2_000_000

class Rejected(ValueError):
    pass

def require(ok, msg):
    if not ok:
        raise Rejected(msg)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def pairs(items):
    out = {}
    for k, v in items:
        require(k not in out, "duplicate manifest key")
        out[k] = v
    return out

def parse(data):
    return json.loads(data.decode("utf-8"), object_pairs_hook=pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(Rejected("nonfinite number")))

def blob(repo, pin, path):
    env = {k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    cmd = ["git", "--no-replace-objects", "-C", str(repo)]
    meta = subprocess.run(cmd + ["ls-tree", pin, "--", path], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=30).stdout
    require(meta.startswith((b"100644 blob ", b"100755 blob ")) and
            meta.rstrip(b"\n").endswith(b"\t" + path.encode()), "source is not a regular tracked file")
    data = subprocess.run(cmd + ["show", pin + ":" + path], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=30).stdout
    require(len(data) <= LIMIT, "source exceeds size limit")
    return data

def expected(repo):
    return {name: blob(repo, pin, path) for name, (pin, path) in PROFILE.items()}

def manifest(data):
    return {"schema_version": 1, "profile": "DIY-VER-003-v1",
            "acceptance": "PENDING", "files": {
                name: {"commit": PROFILE[name][0], "source": PROFILE[name][1],
                       "bytes": len(value), "sha256": digest(value)}
                for name, value in sorted(data.items())}}

def read_regular(path):
    require(not path.is_symlink() and path.is_file(), "nonregular file")
    with path.open("rb") as f:
        data = f.read(LIMIT + 1)
    require(len(data) <= LIMIT, "size limit")
    return data

def build(repo, dest):
    data = expected(repo)
    dest.mkdir(parents=False, exist_ok=False)
    for name, value in data.items():
        p = dest / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(value)
    (dest / MANIFEST).write_text(json.dumps(manifest(data), sort_keys=True, indent=2) + "\n",
                                 encoding="utf-8")
    return verify(repo, dest)

def inventory(root):
    require(not root.is_symlink() and root.is_dir(), "invalid package root")
    files, dirs = set(), set()
    for parent, names, items in os.walk(root, followlinks=False):
        for n in names:
            p = Path(parent) / n
            require(stat.S_ISDIR(p.lstat().st_mode), "nonregular directory")
            dirs.add(p.relative_to(root).as_posix())
        for n in items:
            p = Path(parent) / n
            require(stat.S_ISREG(p.lstat().st_mode), "nonregular file")
            files.add(p.relative_to(root).as_posix())
    return files, dirs

def verify(repo, root):
    names = set(PROFILE) | {MANIFEST}
    dirs = {p.as_posix() for name in names for p in Path(name).parents if p != Path(".")}
    require(inventory(root) == (names, dirs), "package inventory mismatch")
    data = expected(repo)
    got = parse(read_regular(root / MANIFEST))
    # Canonical JSON comparison avoids Python bool/int equality and rejects added keys.
    require(json.dumps(got, sort_keys=True) == json.dumps(manifest(data), sort_keys=True),
            "manifest differs from independently pinned profile")
    for name, value in data.items():
        require(read_regular(root / name) == value, "artifact mismatch: " + name)
    return {"status":"PINNED_PACKAGE_MATCH", "payload_files":len(PROFILE),
            "acceptance":"PENDING", "independent_review":False, "release_authority":False,
            "checker_execution_verified":False}

def main(argv):
    if len(argv) != 4 or argv[1] not in ("build", "verify"):
        print("usage: package.py build|verify REPOSITORY PACKAGE_DIR", file=sys.stderr)
        return 2
    try:
        fn = build if argv[1] == "build" else verify
        print(json.dumps(fn(Path(argv[2]).resolve(), Path(argv[3]).absolute()), sort_keys=True))
    except (ValueError, OSError, subprocess.SubprocessError, RecursionError, TypeError) as e:
        print("REJECT: " + str(e), file=sys.stderr)
        return 1
    return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv))
