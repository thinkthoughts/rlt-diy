import json
import tempfile
import unittest
from pathlib import Path
from package import build, verify, PROFILE, MANIFEST, Rejected, main

ROOT = Path(__file__).resolve().parents[2]

class Checks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dest = Path(self.tmp.name) / "bundle"
        build(ROOT, self.dest)

    def reject(self):
        with self.assertRaises(Rejected):
            verify(ROOT, self.dest)

    def mutate_manifest(self, fn):
        p = self.dest / MANIFEST
        m = json.loads(p.read_text())
        fn(m)
        p.write_text(json.dumps(m))

    def test_positive(self):
        r = verify(ROOT, self.dest)
        self.assertEqual(r["payload_files"], 18)
        self.assertEqual(r["acceptance"], "PENDING")
        self.assertFalse(r["release_authority"])

    def test_gate(self):
        self.assertEqual(main(["package.py","verify",str(ROOT),str(self.dest)]),2)

    def test_empty_manifest(self):
        self.mutate_manifest(lambda m: m["files"].clear())
        self.reject()

    def test_missing_manifest_entry(self):
        self.mutate_manifest(lambda m: m["files"].pop(next(iter(PROFILE))))
        self.reject()

    def test_extra_manifest_entry(self):
        self.mutate_manifest(lambda m: m["files"].update({"extra":{}}))
        self.reject()

    def test_duplicate_key(self):
        p = self.dest / MANIFEST
        p.write_text('{"files":{},"files":{}}')
        self.reject()

    def test_missing_payload(self):
        (self.dest / next(iter(PROFILE))).unlink()
        self.reject()

    def test_extra_payload(self):
        (self.dest / "extra").write_text("extra")
        self.reject()

    def test_extra_directory(self):
        (self.dest / "extra").mkdir()
        self.reject()

    def test_tamper_payload(self):
        p = self.dest / next(iter(PROFILE))
        p.write_bytes(p.read_bytes() + b" ")
        self.reject()

    def test_joint_tamper(self):
        import hashlib
        name = next(iter(PROFILE))
        p = self.dest / name
        data = p.read_bytes() + b" "
        p.write_bytes(data)
        self.mutate_manifest(lambda m: m["files"][name].update(
            {"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}))
        self.reject()

    def test_symlink(self):
        p = self.dest / next(iter(PROFILE))
        p.unlink()
        p.symlink_to(self.dest / MANIFEST)
        self.reject()

    def test_invalid_path(self):
        self.mutate_manifest(lambda m: m["files"].update({"../outside":{}}))
        self.reject()

    def test_approval(self):
        self.mutate_manifest(lambda m: m.update({"acceptance":"APPROVED"}))
        self.reject()

    def test_no_overwrite(self):
        with self.assertRaises(FileExistsError):
            build(ROOT, self.dest)

if __name__ == "__main__":
    unittest.main()
