# DIY-D1-002 — Synthetic distribution correspondence reference verifier

Candidate; unmerged. Python 3.8+ standard library only. This is a deliberately bounded subset of DIY-D1-001. A separately supplied synthetic fixture is the assumed reference for the complete eligible set, rule and output records. No trust in external observations, signatures, or real transactions is established.

Rule: floor(units × numerator / denominator) independently for each row; nonnegative integer base units, bounded to signed-64-bit maximum, exact Python intermediate arithmetic. Shared output allocation must sum exactly to its fixture amount. No adjustments, fees, cross-batch replay, privacy proofs or actual chain finality implemented. Synthetic network only; no real addresses, wallets or keys. Fixture and batch can be jointly falsified; this is not a signature or source-authentication mechanism.

Run from this directory:

    python3 -m unittest -v
    python3 verify.py batch.json fixture.json
    echo "Gate exit: $?"

Expected synthetic result: 3 rows, 2 outputs, 23 base units, SYNTHETIC_MATCH, PENDING. Exit 2 intentionally means incomplete acceptance (also usage error); reject exits 1. No exit 0 path. Tests are authored with the verifier; independent execution and audit pending.

Next: independent adversarial review, canonical signed-byte/key authorization specification, source snapshot identity and cross-batch replay policy. No real payout audit or sustainability claim.
