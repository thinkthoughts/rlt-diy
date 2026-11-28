# DIY-VER-002 — Frozen evidence inventory validator

Candidate, unmerged. Python 3.8+ and Git. This first validator is deliberately specific to DIY-VER-001 at 6cf606def424a512efae27af460a9cf89f4cda9b. It does not implement a general JSON Schema engine, signature authentication, independent reviewer authority, or a release approval path.

The three tracked register/schema/evidence files must match exact bytes from the pinned Git commit. The validator also checks fixed record and axis inventories, candidate and specification references, pending-only acceptance, the single permitted reported software pass, evidence reference and reported test counts, and physical-validation boundaries. It emits SHA-256 hashes of the compared bytes. Git object availability and trusted local Git/runtime are prerequisites; the candidate pins are recorded references, not independently fetched or executed by this tool. A maliciously modified checker or compromised local environment is outside this model. The pinned baseline is an authority decision for this milestone, not an assertion of truth of the operator report.

Run from this directory in a complete clone:

    python3 -m unittest -v
    python3 verify.py ../..
    echo "Gate exit: $?"

Expected: FROZEN_INVENTORY_MATCH, 2 records, 20 axes, 1 reported pass, 19 pending, acceptance PENDING, exit 2. Invalid records exit 1; usage exit 2. There is no release approval exit 0. Sixteen test methods authored; execution and independent audit pending. No changes to the frozen register or evidence bytes. No new D1 execution or S1 checkout identity claim.

Future work: generalized versioned inventories, artifact identity verification across repositories, authorized review records, explicit deferral decisions, scope-specific acceptance policy and independent checker audit. Do not generalize this baseline-specific validator into release authority without a separate reviewed specification.
