# RLT integration contract (proposed)

Keep the author paper, application mathematics and trusted checker distinct.

| Layer | Location | Responsibility |
|---|---|---|
| Original scientific source | application source manifest | version, locator, hash, rights |
| Formalization companion | application docs/ and claims/ | faithful statements and explicit extensions |
| Lean | application lean/ | mathematics outside or inside RLT's supported fragment |
| RLT | application proofs/ plus pinned upstream checker | independently checked supported expressions |
| Engineering | application code and tests | implementation and traceability |
| Physical evidence | application evidence register | calibration, raw records, validation |

Each obligation carries a stable ID, source location, original meaning, formal statement, premises, dependencies, verification method, artifact locator, tool/version, result and limitations. Use the actual RLT file formats and CLI at the pinned revision; this document does not define a new kernel syntax.

An application may depend on RLT as an external checker; no fork or kernel change is required. A Lean theorem may be linked as external evidence, but is not an RLT kernel proof unless independently expressed and checked by RLT. Where translations are proposed, state and verify their correspondence. Unsupported domains remain explicitly open for RLT. A general kernel extension requires a separate upstream proposal and audit.

Suggested independent status axes: source fidelity, analytical proof, Lean check, RLT check, software test, physical validation. Each may be pending, passed within stated scope, failed, unsupported or not applicable; no overall pass may conceal an open dependency.
