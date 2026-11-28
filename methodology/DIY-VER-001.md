# DIY-VER-001 — Common evidence and acceptance architecture

Proposed extension of [DIY-002](DIY-002.md) and the [RLT integration contract](../specifications/RLT-INTEGRATION.md), 2026-11-28. No new RLT kernel syntax or release authority.

## Identity and scope

A record binds a named obligation and versioned specification to a candidate repository, immutable commit and artifact locators. A future acceptance record must additionally pin exact artifact digests, toolchain, commands, raw evidence, premises, units, source rights and dependencies. A repository pin is not proof that a reported execution used that checkout. Preserve reported and observed identity separately.

## Evidence axes

- statement_identity
- source_fidelity
- analytical_proof
- lean_check
- rlt_check
- software_execution
- implementation_correspondence
- external_observation
- physical_validation
- independent_review

Statuses: PENDING (no resolved evidence); REPORTED_PASS (attributed report, not independently verified); SCOPED_PASS (reviewed evidence for named scope); FAIL; UNSUPPORTED; NOT_APPLICABLE (requires explicit justification). These are independent axes, not an ordinal score. Synthetic fixtures cannot establish external observation or physical validation. Evidence records distinguish author, operator, reviewer and execution environment. Retain raw evidence or a privacy-preserving locator/digest; never publish private identifiers by default.

## Acceptance

All records start PENDING. A future release verifier must reject absent or mismatched evidence, unsupported required obligations, unapproved deferrals, stale identity, failed required axes and missing independent review. Approval must bind the reviewed bytes, scope, reviewer independence and explicit decision. No self-approval. An approved synthetic arithmetic scope would not imply an approved real-world application. The v1 schema only describes record structure; schema validation alone cannot confer authority. No executable release acceptance gate is implemented in this milestone.

## Initial records

The [register](../research/diy-ver-001/register.json) pins D1 and S1 research candidates on their respective unmerged branches. D1 execution remains pending. S1 operator-reported VPS output shows twelve passing tests and gate exit 2; exact executed checkout, interpreter and full commands not recorded. See [transcript record](../research/diy-ver-001/evidence/s1-vps-001.json). No independent audit or physical acceptance.

## Next

Implement an explicit inventory validator and negative controls on a separate branch. Bind artifact digests and acceptance decisions; distinguish malformed records from pending acceptance. Require independent review before activating any release approval path.
