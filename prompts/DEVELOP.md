# Reusable AI-assisted development prompts

## Author intake
Read the registered leading specifications, identify exact source locations and distinguish original claims from your proposed extensions. Produce a dependency-ordered roadmap, explicit assumptions, definitions, counterexamples and proof/physical obligations. Do not assume the hypothesis is true. Ask the author only for missing decisions that materially affect implementation.

## Implementation (Claude or another coding agent)
Inspect the actual repository and pinned RLT capabilities. Start a separate branch from the confirmed baseline. Select one bounded milestone. Write its specification and tests before implementation; formalize supported mathematical statements in Lean and RLT separately. Preserve source fidelity, report unsupported fragments, pin dependencies, execute checks, and record exact commands, results and commit. Do not modify the RLT kernel, claim unexecuted checks, merge, or publish without approval.

## Independent audit
Review the source and exact implementation commit independently. Challenge assumptions, statement fidelity, model/code correspondence, provenance, failure paths and verification policy. Reproduce checks from clean inputs. Report numbered findings with severity, evidence, repairs and remaining scope. Do not count simulation as physical validation. Leave merge decision to project owner.

## Handoff
Prepare author-owned repository setup, instructions, roadmap, reproducible checks, outstanding decisions, licenses and attribution. Distinguish public reference implementation from official product. Agree terms before transferring domains or undertaking proprietary work.
