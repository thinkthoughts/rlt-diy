# DIY-S1-002 — Synthetic resource-to-useful-work accounting

Proposed executable subset of DIY-S1-001; unmerged. Python 3.8+ standard library. All records are invented, not physical measurements. Exact rational arithmetic via Fraction; nonnegative decimal strings, bounded sizes. Intervals are contiguous from elapsed second zero; the declared end is not independently authenticated. Energy is kWh, intensity gCO2e/kWh, embodied allocation gCO2e, and work is a positive accepted functional-unit quantity. Lower/upper endpoints are assumed jointly safe enclosures, not statistical confidence intervals. Products and sums use nonnegative interval arithmetic; division uses opposite work endpoints. Output rational strings are exact.

Two runs share a declared workload, quality, functional unit, boundary, region and period. These are assumptions, not evidence of equivalence. Different hardware/software are allowed. Source labels do not authenticate meters, grid data or inventory. A strict interval separation is conditional on supplied bounds; overlapping or touching bounds return NOT_RESOLVED_BY_BOUNDS. Missing data rejects rather than silently becoming zero. No real telemetry, calibration, overhead allocation, repeatability or standards-conformity checks implemented. No full acceptance exit 0.

Run from this directory:

    python3 -m unittest -v
    python3 verify.py fixture.json
    echo "Gate exit: $?"

Expected baseline energy 9–11 kWh, candidate 5–7 kWh; baseline emissions/work 27–38.5 gCO2e, candidate 17–26.5. Both comparisons STRICTLY_LOWER on synthetic assumptions. Exit 2 intentionally indicates incomplete acceptance (also usage error); reject exits 1. Tests authored with implementation; execution and independent review pending.

Next: independent adversarial audit; external protocol and workload equivalence checks; meter/time provenance, uncertainty and allocation models, consent and repeated comparisons. No sustainability improvement inferred.
