import copy
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from verify import verify, load, Rejected, main, relation, div, q
ROOT = Path(__file__).parent

class Checks(unittest.TestCase):
    def setUp(self):
        self.x = load(ROOT / "fixture.json")

    def test_valid(self):
        r = verify(self.x)
        self.assertEqual(r["baseline"]["energy_kwh"], ["9", "11"])
        self.assertEqual(r["baseline"]["operational_gco2e"], ["2300", "3350"])
        self.assertEqual(r["baseline"]["emissions_per_work"], ["27", "77/2"])
        self.assertEqual(r["candidate"]["energy_kwh"], ["5", "7"])
        self.assertEqual(r["candidate"]["emissions_per_work"], ["17", "53/2"])
        self.assertEqual(r["comparison"], {"energy_per_work":"STRICTLY_LOWER",
                         "emissions_per_work":"STRICTLY_LOWER"})
        self.assertEqual(r["acceptance"], "PENDING")
        self.assertFalse(r["physical_validation"])
        self.assertFalse(r["comparability_verified"])

    def test_exact_decimal(self):
        self.assertEqual(q("0.1") + q("0.2"), Fraction(3, 10))

    def test_positive_work(self):
        self.x["candidate"]["work"] = ["0", "1"]
        with self.assertRaises(Rejected):
            verify(self.x)

    def test_uncertain_work(self):
        self.assertEqual(div((Fraction(10), Fraction(20)),
                             (Fraction(2), Fraction(5))), (2, 10))

    def test_overlap_and_touch(self):
        self.assertEqual(relation((1, 2), (2, 3)), "NOT_RESOLVED_BY_BOUNDS")
        self.assertEqual(relation((3, 4), (1, 2)), "STRICTLY_HIGHER")
        self.assertEqual(relation((1, 3), (2, 4)), "NOT_RESOLVED_BY_BOUNDS")

    def test_invalid_decimal(self):
        for x in [True, 1, 0.1, "-1", "NaN", "1e3", "01", "1/2"]:
            with self.subTest(x=x):
                with self.assertRaises(Rejected):
                    q(x)

    def test_inverted(self):
        self.x["baseline"]["embodied_gco2e"] = ["5", "4"]
        with self.assertRaises(Rejected):
            verify(self.x)

    def test_interval_continuity(self):
        for start in [3500, 3700, True]:
            x = copy.deepcopy(self.x)
            x["candidate"]["intervals"][1]["start_s"] = start
            with self.assertRaises(Rejected):
                verify(x)

    def test_missing_data(self):
        del self.x["baseline"]["embodied_gco2e"]
        with self.assertRaises(Rejected):
            verify(self.x)

    def test_duplicate_run(self):
        self.x["candidate"]["id"] = self.x["baseline"]["id"]
        with self.assertRaises(Rejected):
            verify(self.x)

    def test_duplicate_json_key(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t)/"bad.json"
            p.write_text('{"x":1,"x":2}')
            with self.assertRaises(Rejected):
                load(p)

    def test_gate(self):
        self.assertEqual(main(["verify.py", str(ROOT/"fixture.json")]), 2)

if __name__ == "__main__":
    unittest.main()
