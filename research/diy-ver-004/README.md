# DIY-VER-004 — Offline verification commitments

Candidate, unmerged. Python 3.8+ standard library. Uses the fixed 19-file VER-003 v1 package (18 payloads plus manifest). No Git, network, package code execution or archive extraction needed by the offline checker.

## Trust and delivery

1. A sender uses the pinned VER-003 checker to build and verify the source-backed package. Review provenance and scope separately.
2. Run offline.py issue to snapshot the package into a separate commitment file. It checks internal manifest correspondence, not source provenance. The resulting SHA-256 of the exact commitment bytes is an external anchor, not a signature.
3. Deliver the package and commitment file. Communicate the anchor via a separately authenticated, trusted channel. The recipient must obtain and trust the checker independently; do not use a checker supplied only in the untrusted package.
4. The recipient supplies the trusted anchor explicitly to offline.py verify. Exact inventory, regular file types, manifest correspondence and all committed bytes must match. No release approval is possible.

If the sender, package, commitment and anchor are jointly substituted, the checker cannot detect that without trusted external identity. An issuer can commit arbitrary internally consistent content. Verification does not authenticate issuer, prove source identities or replay the checkers. It assumes a stable local filesystem and trusted Python/checker; concurrent mutation and host compromise are outside scope. SHA-256 collision/preimage resistance assumed. No signature or independent review envelope implemented yet.

## Commands

From research/diy-ver-004, assuming a previously built VER-003 package:

    python3 -m unittest -v
    python3 offline.py issue /tmp/diy-package-v1 /tmp/diy-commitment-v1.json
    echo "Gate exit: $?"

Copy the emitted anchor independently. On recipient machine, with independently obtained offline.py:

    python3 offline.py verify /tmp/diy-package-v1 /tmp/diy-commitment-v1.json TRUSTED_SHA256
    echo "Gate exit: $?"

Replace TRUSTED_SHA256 with the independently obtained 64-character lowercase digest. Use a new commitment path. Expected OFFLINE_INTEGRITY_MATCH, files=19, acceptance=PENDING, exit 2. Rejection exit 1; usage exit 2. Seventeen test methods authored with entirely synthetic fixture bytes. Actual source-backed package execution and independent audit remain pending.

## Evidence

The separate VER-003 operator-reported test result is preserved in evidence/ver003-vps-001.json. Prior frozen evidence remains untouched. No standalone build/verify transcript or exact executed checkout was supplied. This new evidence is not in the v1 package; a later independently pinned profile may include it.

Next: independently reproduce and audit; VER-005 authenticated reviewer envelope with explicit trust roots, reviewed byte identities and scoped decisions.
