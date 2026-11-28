# DIY-VER-003 — Portable verification package profile v1

Candidate, unmerged. A portable directory of 18 pinned payload files and one generated manifest. Contains the leading D1/S1 specifications, synthetic checkers/fixtures/tests, VER-001 evidence records and VER-002 checker. This is a fixed-profile prototype, not a general archive format or release approval system.

The expected inventory and source commit/path mapping live in the external checker, not in the supplied package. Verify exact file AND directory sets, regular files only, canonical manifest content and exact bytes against independently pinned Git objects. An attacker changing both a payload and its manifest hash cannot satisfy that reference. Reject empty/missing/extra entries, duplicate JSON keys, symlinks, extra files/directories and fabricated approval. No archive extraction, untrusted code execution or network operations.

The directory is portable for inspection; verification requires a trusted checker, Git and access to all three pinned source commits in a local repository. Fetch D1 and S1 branches if absent. Copied VER-002 scripts require their original Git repository layout to execute; this bundle is not a standalone runtime for all three checkers. No package signature, independent authority or runtime attestation yet. Local filesystem races/host compromise outside scope.

The new operator-reported VER-002 transcript is preserved separately at evidence/ver-vps-001.json in this branch, without altering the frozen VER-001 register. It is not part of the v1 package profile; a future profile must pin it after this commit exists. No circular self-hash.

From a full clone, at repository root:

    git fetch origin diy-d1-002 diy-s1-002
    cd research/diy-ver-003
    python3 -m unittest -v
    python3 package.py build ../.. /tmp/diy-package-v1
    echo "Gate exit: $?"
    python3 package.py verify ../.. /tmp/diy-package-v1
    echo "Gate exit: $?"

Choose a fresh destination directory. Expected 18 payload files, PINNED_PACKAGE_MATCH, PENDING, exit 2. Rejection exit 1; usage exit 2. No exit 0 approval. Fifteen test methods authored; execution pending. The package checker itself must be independently pinned and reviewed before distribution. No claim of physical correspondence.

Next: review and execute tests, pin the package checker and VER-002 transcript in a successor profile, design an offline externally anchored digest inventory and independent review envelope. Preserve profile v1.
