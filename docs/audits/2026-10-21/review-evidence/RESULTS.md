# Human review evidence implementation results

Date: 2026-10-21
Work: WP-03, F-03, FR-09, TR-06, EX-06

## Implemented

ADR-003 records the contract before implementation. Added opt-in
human_review_evidence version 1.0, explicit per-check rubrics, source excerpts and
response origins, snapshots and hashes, pending/not_run preparation and a read-only
validate-review command. Completion rejects unresolved states, missing response
quotes, reviewer metadata and missing source evidence. Current-folder comparison
is optional and rejects stale reviews. Existing review sheets and deterministic
report shapes remain unchanged; the viewer does not import human reviews.

Refactored the existing package validator into reusable validate_data and kept
the file-based validate entry point. Updated canonical evaluation skill and synced
eight adapters. No changes to the seven-file package schema or user projects.

## Executed evidence

- Existing baseline from I20: 37 passing tests.
- First implementation run: 47 tests passed; no failing-first evidence claimed.
- Added CLI invocation from another directory: final 48 tests passed.
- Eight adapter checks passed; fictional package strict coverage and blank template
  structural validation passed.
- Generated pending-example.json through the actual CLI and validated it. It has
  six pending judgments, no reviewer, no review date and no pass/fail judgments.
- Tests exercise complete synthetic records containing failures. Those are
  validator fixtures, not completed human reviews or model outputs.
- Rejections exercised: snapshot/hash inconsistency, duplicate/missing/unknown
  judgments, missing response, invalid metadata/timezone, whitespace rationale,
  invented quote, missing source evidence, unknown origin, unresolved completion,
  legacy/unsupported record shape, staleness and overwrite attempts.

## Limits and next action

No model call, new agent journey, independent human review or learner session ran.
Human authorship and identity are declared, not authenticated. Hashes do not stop
someone replacing evidence and recomputing hashes. Source excerpts are supplied
explicitly and not independently authenticated. Structural completion cannot
establish the correctness or consistency of the judgments.

The provisional fictional rubrics and grounded/invented/borderline examples are
ready for two independent human reviewers. Record disagreements before claiming
calibrated review quality. F-03's software evidence gap is addressed in this opt-in
path; WP-03 human calibration and broader product acceptance remain open.
