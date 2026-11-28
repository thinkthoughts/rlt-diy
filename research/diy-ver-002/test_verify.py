import copy
import tempfile
import unittest
from pathlib import Path
from verify import (BASE, REGISTER, SCHEMA, EVIDENCE, PATHS, git,
                    parse, check_records, verify, main, Rejected, frozen)

ROOT = Path(__file__).resolve().parents[2]

class Checks(unittest.TestCase):
    def setUp(self):
        self.r = parse(git(ROOT, "show", BASE + ":" + REGISTER))
        self.e = parse(git(ROOT, "show", BASE + ":" + EVIDENCE))

    def test_current_inventory(self):
        out = verify(ROOT)
        self.assertEqual((out["records"], out["axes"], out["reported_pass"],
                          out["pending_axes"]), (2, 20, 1, 19))
        self.assertFalse(out["release_authority"])
        self.assertEqual(out["acceptance"], "PENDING")

    def test_gate(self):
        self.assertEqual(main(["verify.py", str(ROOT)]), 2)

    def test_missing_record(self):
        self.r["records"].pop()
        with self.assertRaises(Rejected):
            check_records(self.r, self.e)

    def test_duplicate_record(self):
        self.r["records"][1] = copy.deepcopy(self.r["records"][0])
        with self.assertRaises(Rejected):
            check_records(self.r, self.e)

    def test_status_promotions(self):
        for axis in ("software_execution", "physical_validation", "independent_review"):
            r = copy.deepcopy(self.r)
            r["records"][1]["axes"][axis]["status"] = "SCOPED_PASS"
            with self.assertRaises(Rejected):
                check_records(r, self.e)

    def test_approval(self):
        self.r["records"][0]["acceptance"] = {"decision":"APPROVED", "reviewer":"fake",
                                              "review_record":"fake.json"}
        with self.assertRaises(Rejected):
            check_records(self.r, self.e)

    def test_wrong_candidate(self):
        self.r["records"][1]["candidate"]["commit"] = "0" * 40
        with self.assertRaises(Rejected):
            check_records(self.r, self.e)

    def test_evidence_reference(self):
        self.r["records"][1]["axes"]["software_execution"]["evidence"] = ["../outside"]
        with self.assertRaises(Rejected):
            check_records(self.r, self.e)

    def test_missing_axis(self):
        del self.r["records"][0]["axes"]["lean_check"]
        with self.assertRaises(Rejected):
            check_records(self.r, self.e)

    def test_missing_obligation(self):
        self.r["records"][1]["open_obligations"].pop()
        with self.assertRaises(Rejected):
            check_records(self.r, self.e)

    def test_forged_execution(self):
        self.e["observed_checkout"] = self.e["candidate_reference"]
        with self.assertRaises(Rejected):
            check_records(self.r, self.e)

    def test_test_counts(self):
        self.e["tests"]["failures"] = True
        with self.assertRaises(Rejected):
            check_records(self.r, self.e)

    def test_physical_claim(self):
        self.e["result"]["physical_validation"] = True
        with self.assertRaises(Rejected):
            check_records(self.r, self.e)

    def test_duplicate_json_key(self):
        with self.assertRaises(Rejected):
            parse(b'{"x":1,"x":2}')

    def test_nonfinite(self):
        with self.assertRaises(Rejected):
            parse(b'{"x":NaN}')

    def test_frozen_tamper_and_symlink(self):
        # Temporary local clone; do not modify source checkout.
        with tempfile.TemporaryDirectory() as t:
            import subprocess
            root = Path(t) / "clone"
            subprocess.run(["git", "clone", "--quiet", "--no-hardlinks",
                            str(ROOT), str(root)], check=True)
            p = root / EVIDENCE
            p.write_bytes(p.read_bytes() + b" ")
            with self.assertRaises(Rejected):
                frozen(root, EVIDENCE)
            p.unlink()
            p.symlink_to(root / REGISTER)
            with self.assertRaises(Rejected):
                frozen(root, EVIDENCE)

if __name__ == "__main__":
    unittest.main()
