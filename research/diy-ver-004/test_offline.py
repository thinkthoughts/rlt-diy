import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from offline import NAMES, PROFILE, issue, verify, main, Rejected, encode

class Checks(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name)/"package"
        self.root.mkdir()
        self.commit = Path(t.name)/"commitment.json"
        files = {}
        for name in NAMES:
            if name == "manifest.json":
                continue
            p = self.root/name
            p.parent.mkdir(parents=True, exist_ok=True)
            data = ("synthetic test: "+name).encode()
            p.write_bytes(data)
            files[name] = {"commit":"a"*40,"source":name,"bytes":len(data),
                           "sha256":hashlib.sha256(data).hexdigest()}
        self.manifest = self.root/"manifest.json"
        self.manifest.write_bytes(encode({"schema_version":1,"profile":PROFILE,
                                         "acceptance":"PENDING","files":files}))
        self.anchor = issue(self.root,self.commit)["anchor_sha256"]

    def reject(self):
        with self.assertRaises(Rejected):
            verify(self.root,self.commit,self.anchor)

    def test_positive(self):
        r = verify(self.root,self.commit,self.anchor)
        self.assertEqual(r["files"],19)
        self.assertEqual(r["acceptance"],"PENDING")
        self.assertFalse(r["source_provenance_verified"])
        self.assertFalse(r["issuer_authenticated"])

    def test_gate(self):
        self.assertEqual(main(["offline.py","verify",str(self.root),str(self.commit),self.anchor]),2)

    def test_wrong_anchor(self):
        self.anchor = "0"*64
        self.reject()

    def test_malformed_anchor(self):
        self.anchor = "xyz"
        self.reject()

    def test_payload_tamper(self):
        (self.root/NAMES[0]).write_bytes(b"changed")
        self.reject()

    def test_joint_tamper(self):
        p = self.root/NAMES[0]
        p.write_bytes(b"changed")
        m = json.loads(self.manifest.read_bytes())
        m["files"][NAMES[0]].update(bytes=7,sha256=hashlib.sha256(b"changed").hexdigest())
        self.manifest.write_bytes(encode(m))
        self.reject()

    def test_reissued_commitment(self):
        p = self.root/NAMES[0]
        p.write_bytes(b"changed")
        m = json.loads(self.manifest.read_bytes())
        m["files"][NAMES[0]].update(bytes=7,sha256=hashlib.sha256(b"changed").hexdigest())
        self.manifest.write_bytes(encode(m))
        self.commit.unlink()
        issue(self.root,self.commit)
        self.reject()

    def test_commitment_tamper(self):
        self.commit.write_bytes(self.commit.read_bytes()+b" ")
        self.reject()

    def test_missing_file(self):
        (self.root/NAMES[0]).unlink()
        self.reject()

    def test_extra_file(self):
        (self.root/"extra").write_text("extra")
        self.reject()

    def test_extra_dir(self):
        (self.root/"extra").mkdir()
        self.reject()

    def test_symlink(self):
        p = self.root/NAMES[0]
        p.unlink()
        p.symlink_to(self.manifest)
        self.reject()

    def test_empty_commitment(self):
        self.commit.write_bytes(b"{}")
        self.anchor = hashlib.sha256(b"{}").hexdigest()
        self.reject()

    def test_duplicate_commitment_key(self):
        self.commit.write_bytes(b'{"files":{},"files":{}}')
        self.anchor = hashlib.sha256(self.commit.read_bytes()).hexdigest()
        self.reject()

    def test_forged_approval(self):
        m = json.loads(self.commit.read_bytes())
        m["acceptance"] = "APPROVED"
        self.commit.write_bytes(encode(m))
        self.anchor = hashlib.sha256(self.commit.read_bytes()).hexdigest()
        self.reject()

    def test_refuse_overwrite(self):
        with self.assertRaises(FileExistsError):
            issue(self.root,self.commit)

    def test_refuse_inside_package(self):
        with self.assertRaises(Rejected):
            issue(self.root,self.root/"commitment.json")

if __name__ == "__main__":
    unittest.main()
