# FNS-003 — Fractal Neural Synthesis

Status: frozen technical candidate RLT-FNS-001h available for independent review. Collaboration has not been agreed. Independent clean replay, acceptance, benchmark reproduction and physical energy measurement remain pending.

## Leading specification

Volkan Dagli, Zerrin Dagli and Daghan Dagli, *Fractal Neural Synthesis: Constant-Storage Procedural Weight Derivation via Complex Quadratic Boundary Dynamics*, v4.0. [arXiv:2611.32393](https://arxiv.org/abs/2611.32393); [version DOI](https://doi.org/10.5281/zenodo.24495977).

- Upstream: https://github.com/pCwOrM/fractal-neural-synthesis
- Initial source revision: `be57087b8b368490e6ed49deb7ed60f0ff0b2fd0` (repository inventory inspected 2026-11-27; full paper and proof audit pending).
- License: [BSL 1.1](https://github.com/pCwOrM/fractal-neural-synthesis/blob/be57087b8b368490e6ed49deb7ed60f0ff0b2fd0/LICENSE), permitting noncommercial academic inspection and reproduction; commercial deployment restricted, patent notice applies. Review rights before redistribution or product development.
- Companion repository: https://github.com/thinkthoughts/rlt-fns. [Frozen candidate](https://github.com/thinkthoughts/rlt-fns/tree/7015035e8b78c3e75f428316a81d9b7f4701b6ff); 12 obligations, 8 source artifacts, 23 Lean theorems, 24 declaration identities, 14 negative integrity probes and two positive controls, 74 locally matched release artifacts.

## Leading reading point

Reduced storage alone is insufficient to establish reduced energy consumption.

A 24-byte coordinate seed is distinct from total persistent model storage, working memory, firmware, readout parameters and computation. Compare equal workload and output quality, counting memory traffic, latency, iteration costs and measured energy within declared system boundaries. Edge-device results are not evidence of data-center savings without a separate correspondence study.

## Available for review: RLT-FNS-001h

Three correction candidates: exact cross-cell coordinate collision (M=3, indices 1 and 2); a Lean counterexample to the universal C¹ quadratic Taylor remainder; a positive rational interval enclosure of the leading 3×3 determinant of the exact centered Vogel affine test matrix (0.001075694 < D < 0.001075695). The last establishes exact rank at least three for that matrix, not the empirical effective rank of the actual generators.

[Internal audit](https://github.com/thinkthoughts/rlt-fns/blob/7015035e8b78c3e75f428316a81d9b7f4701b6ff/docs/RLT-FNS-001h-B-INTERNAL-AUDIT.md) · [Vogel certificate](https://github.com/thinkthoughts/rlt-fns/blob/7015035e8b78c3e75f428316a81d9b7f4701b6ff/docs/RLT-FNS-001g-C-VOGEL.md) · [Audit repairs](https://github.com/thinkthoughts/rlt-fns/blob/7015035e8b78c3e75f428316a81d9b7f4701b6ff/docs/RLT-FNS-001h-B1-REPAIRS.md) · [Frozen manifest](https://github.com/thinkthoughts/rlt-fns/blob/7015035e8b78c3e75f428316a81d9b7f4701b6ff/claims/release-artifacts.json). User-reported VPS release gate reached pending-review refusal (exit 1) after matching all 74 artifacts. Independent replay and acceptance pending; full normal verification transcript not separately supplied.

Authors and interested researchers are invited to inspect, reproduce or challenge the work independently via [GitHub issues](https://github.com/thinkthoughts/rlt-fns/issues). Further collaboration is open to discussion. No endorsement implied.

## Initial assessment: RLT-FNS-001 (historical)

Preliminary findings and next specification: [assessment](https://github.com/thinkthoughts/rlt-fns/blob/cc99046f74983b47815f2aba633ce05ef33a93ac/docs/RLT-FNS-001-ASSESSMENT.md), [obligations](https://github.com/thinkthoughts/rlt-fns/blob/cc99046f74983b47815f2aba633ce05ef33a93ac/claims/obligations.json), [001b](https://github.com/thinkthoughts/rlt-fns/blob/cc99046f74983b47815f2aba633ce05ef33a93ac/docs/RLT-FNS-001b-SPEC.md). Selected manuscript sections and source code inspected, with Taylor remainder and sampling-layout qualifications; full audit and execution pending.

Read the complete pinned paper and register exact claim locations, source hashes and dependencies. Inspect existing Lean declarations, axioms and statement correspondence; distinguish exact recurrence mathematics from numerical arithmetic and benchmark evidence. Reproduce only after pinning dependencies and defining the acceptance criteria. No kernel changes or application implementation in this registration.

| Artifact | Role |
|---|---|
| [paper1_v4/latex/body.tex](https://github.com/pCwOrM/fractal-neural-synthesis/blob/be57087b8b368490e6ed49deb7ed60f0ff0b2fd0/paper1_v4/latex/body.tex) | Written mathematical specification |
| [zenodo_lean4_package/Verify.lean](https://github.com/pCwOrM/fractal-neural-synthesis/blob/be57087b8b368490e6ed49deb7ed60f0ff0b2fd0/zenodo_lean4_package/Verify.lean) | Existing Lean verification; scope to be audited |
| [paper1_v4/experiments/run_paper1_v4_suite.py](https://github.com/pCwOrM/fractal-neural-synthesis/blob/be57087b8b368490e6ed49deb7ed60f0ff0b2fd0/paper1_v4/experiments/run_paper1_v4_suite.py) | Experimental reproduction |
| [paper1_v4/data/paper1_v4_results.json](https://github.com/pCwOrM/fractal-neural-synthesis/blob/be57087b8b368490e6ed49deb7ed60f0ff0b2fd0/paper1_v4/data/paper1_v4_results.json) | Author-reported records |
| [src/mandelbrot_core.py](https://github.com/pCwOrM/fractal-neural-synthesis/blob/be57087b8b368490e6ed49deb7ed60f0ff0b2fd0/src/mandelbrot_core.py) | Computational implementation |
| [tests/test_fractal_core.py](https://github.com/pCwOrM/fractal-neural-synthesis/blob/be57087b8b368490e6ed49deb7ed60f0ff0b2fd0/tests/test_fractal_core.py) | Existing software tests |

## Proposed roadmap

| Milestone | Verification target |
|---|---|
| RLT-FNS-001 | Mathematical specification and existing Lean proof audit |
| RLT-FNS-002 | Constant-storage and information capacity claims |
| RLT-FNS-003 | Floating-point and Q16.16 implementation correspondence |
| RLT-FNS-004 | Independent benchmark reproduction |
| RLT-FNS-005 | Computational cost and memory traffic |
| RLT-FNS-006 | Energy per useful inference |
| RLT-FNS-007 | Hardware and deployment applicability |

## Foundations

[Clean data centers](../../foundations/clean-datacenters/README.md) and [verified engineering](../../foundations/verified-engineering/README.md). The foundations develop independently of author participation. Any joint development, funding or commercialization requires separate agreement.
