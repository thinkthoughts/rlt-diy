import copy
import json
import tempfile
import unittest
from pathlib import Path
from verify import verify, load, Rejected, main

ROOT = Path(__file__).parent

class Checks(unittest.TestCase):
    def setUp(self):
        self.b = load(ROOT / "batch.json")
        self.f = load(ROOT / "fixture.json")

    def test_valid(self):
        r = verify(self.b, self.f)
        self.assertEqual((r["rows"], r["outputs"], r["total_base_units"]), (3, 2, 23))
        self.assertEqual(r["acceptance"], "PENDING")
        self.assertFalse(r["signature_verified"])
        self.assertFalse(r["chain_verified"])

    def test_permutation(self):
        self.b["rows"].reverse()
        self.assertEqual(verify(self.b, self.f)["total_base_units"], 23)

    def test_gate(self):
        self.assertEqual(main(["verify.py", str(ROOT/"batch.json"), str(ROOT/"fixture.json")]), 2)

    def test_bad_rows(self):
        for k, value in [("units", True), ("amount", 8), ("amount", -1),
                         ("destination", "wrong"), ("participant", "wrong"),
                         ("vout", 9), ("contribution_id", "unknown")]:
            with self.subTest(k=k, value=value):
                b = copy.deepcopy(self.b)
                b["rows"][0][k] = value
                with self.assertRaises(Rejected):
                    verify(b, self.f)

    def test_missing_duplicate(self):
        for rows in [self.b["rows"][:-1], self.b["rows"] + self.b["rows"][:1]]:
            b = copy.deepcopy(self.b)
            b["rows"] = rows
            with self.assertRaises(Rejected):
                verify(b, self.f)

    def test_context_rule(self):
        for k, val in [("network", "mainnet"), ("asset", "OTHER"), ("rule_id", "other"), ("batch_id", "other")]:
            b = copy.deepcopy(self.b)
            b[k] = val
            with self.assertRaises(Rejected):
                verify(b, self.f)

    def test_output_totals(self):
        self.f["outputs"][0]["amount"] += 1
        with self.assertRaises(Rejected):
            verify(self.b, self.f)

    def test_duplicate_fixture(self):
        for k in ["outputs", "contributions"]:
            f = copy.deepcopy(self.f)
            f[k].append(copy.deepcopy(f[k][0]))
            with self.assertRaises(Rejected):
                verify(self.b, f)

    def test_schema(self):
        self.b["unexpected"] = True
        with self.assertRaises(Rejected):
            verify(self.b, self.f)

    def test_zero_denominator(self):
        self.f["rule"]["denominator"] = 0
        with self.assertRaises(Rejected):
            verify(self.b, self.f)

    def test_duplicate_json_key(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t)/"bad.json"
            p.write_text('{"x":1,"x":2}')
            with self.assertRaises(Rejected):
                load(p)

if __name__ == "__main__":
    unittest.main()
