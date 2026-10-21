# ADR-001: Let valid drafts exist before evaluation coverage is complete

Date: 2026-10-21. Status: accepted for the bounded WP-01 experiment.
Implementation: completed; local deterministic acceptance passed (23-test suite).
Agent/learner acceptance remains a separate gate. See ../ITERATIONS.md.
Related: F-01, FR-05 through FR-11, TR-06, EX-06.
This records an engineering decision, not organizational rule approval.

## Question and evidence

Should every saved rule need an evaluation check before a draft can validate?
The brief sequences content standards at stage 2 and checks at stage 5. Current
validate() and status reject that intermediate state. The baseline probe reproduces
the failure. Drafts need trustworthy structure/links without claiming readiness.

## Options

| Option | Benefit | Cost / reason |
|---|---|---|
| Create checks immediately for all new rules | Strong coverage invariant everywhere | Forces a later learning stage into early drafting; incomplete checks may be invented merely to satisfy validation |
| Turn all validation off for drafts | Flexible editing | Hides malformed fields, unknown IDs and broken references |
| Separate structure/links from coverage | Supports staged work while keeping integrity checks | Needs clear command output and an explicit coverage gate |
| Add a full workflow state engine now | Could infer stage-specific constraints | Unnecessary complexity before observing actual learners; reviewed state alone cannot prove work happened |

## Decision

validate(folder) checks schema, unique IDs and existing source/requirement links.
Coverage gaps are returned by a separate helper and shown as draft information.
`validate --require-coverage` retains the prior strict coverage behavior.
`status` remains usable for well-formed partial packages and shows coverage gaps.
`check` and `review` continue to require coverage before preparing execution/review.
No rule is approved, stage advanced, missing check generated, or user file changed
automatically. Invalid references remain errors in every mode.

## Acceptance experiment

Start from the empty template; add one draft content rule at stage 2; save a decision
and next_action; run validate and status; reopen the package and inspect saved state.
Both commands must succeed while showing missing coverage. Strict validation and
execution must fail. Add a linked check and saved response; both strict validation
and execution must then succeed. Replacing the link with an unknown requirement
must still fail. Run existing complete-package tests to detect regressions.

This is a deterministic simulation of staged file editing, not evidence that an
agent asks good questions or that a beginner learns. Those are phase C/H gates.

## Compatibility and follow-up

This relaxes default validate's coverage semantics. Automation depending on the
previous nonzero exit must add --require-coverage. No package fields change and no
migration is required. Existing complete-package reports should be unchanged.
Execution still cannot mean “overall quality passed”; phase D will define that
separately. Review partial-package observations before adding a readiness engine.
