# Focused Codex pilot acceptance ledger

Scope: local Codex pilot, not general release certification. Date: 2026-10-21.

| Claim / requirement | Observed evidence | Remaining gap |
| --- | --- | --- |
| Core local workflow, TR-06/07 | 83 unit/integration tests pass; eight generated adapters match | Not proof of learner understanding or model adherence |
| Portable runtime, PORT-01 | New relocated-bundle test runs initialization, coverage validation, saved-response check, viewer, evidence review and review page; preserves unrelated instructions and bundle hashes | Other operating systems and Python versions untested |
| Installation, TR-08 | Fresh venv dependency installation succeeds using pip's cached official-package wheels; bundled CLI initializes, validates and renders | Not a cache-empty installation; sandbox temp/network restrictions required environment adjustment |
| Codex plugin activation, FR-01 | Codex 0.162.0-alpha.17.2 accepted local marketplace and installed fievel@fievel-local 0.1.0 | Fresh-session behavior assessed separately; desktop UI refresh not observed |
| Sources and quality evidence, SRC-01 | Existing deterministic source and review tests retained | Actual source conversion and human interpretation still need trials |
| Consumer integration, SYS-02 | Export contract is implemented and tested | Real consuming-AI adherence is unproven |
| Product value, FR-12 | A testable hypothesis and comparator plan exist | Jeremy's pilot, independent usability and matched comparisons remain |

A stale WORKFLOW.md statement that no completed-record validation existed was
corrected: evidence-record validation exists, but does not establish judgment
correctness or authenticated human review.

Pilot decision: proceed with local plugin trials. Do not infer general release
readiness from the passing software tests. Model calls are authorized for these
trials; public publication and participant outreach are not.
