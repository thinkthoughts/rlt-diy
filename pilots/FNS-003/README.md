# FNS-003 — Fractal Neural Synthesis

Status: registered independent research pilot; initial assessment planned. Collaboration has not been agreed. No independent reproduction, implementation audit or physical energy measurement is claimed.

## Leading specification

Volkan Dagli, Zerrin Dagli and Daghan Dagli, *Fractal Neural Synthesis: Constant-Storage Procedural Weight Derivation via Complex Quadratic Boundary Dynamics*, v4.0. [arXiv:2611.32393](https://arxiv.org/abs/2611.32393); [version DOI](https://doi.org/10.5281/zenodo.24495977).

- Upstream: https://github.com/pCwOrM/fractal-neural-synthesis
- Initial source revision: `be57087b8b368490e6ed49deb7ed60f0ff0b2fd0` (repository inventory inspected 2026-11-27; full paper and proof audit pending).
- License: [BSL 1.1](https://github.com/pCwOrM/fractal-neural-synthesis/blob/be57087b8b368490e6ed49deb7ed60f0ff0b2fd0/LICENSE), permitting noncommercial academic inspection and reproduction; commercial deployment restricted, patent notice applies. Review rights before redistribution or product development.
- Companion repository `thinkthoughts/rlt-fns` is proposed, not created.

## Leading reading point

Reduced storage alone is insufficient to establish reduced energy consumption.

A 24-byte coordinate seed is distinct from total persistent model storage, working memory, firmware, readout parameters and computation. Compare equal workload and output quality, counting memory traffic, latency, iteration costs and measured energy within declared system boundaries. Edge-device results are not evidence of data-center savings without a separate correspondence study.

## Initial assessment: RLT-FNS-001

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
