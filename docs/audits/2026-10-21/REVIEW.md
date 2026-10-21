# Deliberate review of the initial prototype

Date: 2026-10-21. Reviewer: the implementation agent, reviewing its own work.
This is a self-audit; it is not independent expert review, a learner study, or a
fresh-context agent evaluation. Scope: the original brief, core CLI/schema/tests,
skills, learning content, example artifacts and documentation claims.

## Baseline and method

The original brief is now preserved in ../../PRODUCT-BRIEF.md. Before changing
implementation, recorded SHA-256 hashes of 62 project files in
[baseline-manifest.json](baseline-manifest.json). All project files were untracked
at the time; the manifest is a reference, not a Git snapshot or recoverable commit.
The baseline test run in [baseline-tests.txt](baseline-tests.txt) passed 21 tests.

Reviewed code against intermediate stages as well as finished fixtures. Executed
isolated probes using [reproduce.py](reproduce.py); observed output is preserved in
[baseline-probes.json](baseline-probes.json). Research inspection references and
checksums are in [upstream-inspection.json](upstream-inspection.json). No unrelated
user project was edited; probes use temporary copies under .scratch.

## Findings

| ID / priority | Observed issue and evidence | Effect on a content designer | Disposition |
|---|---|---|---|
| F-01 / high | validate() enforces coverage for every rule, and status calls validate(). A stage-2 draft with one valid rule and no stage-5 checks fails. baseline-probes.json records the exact rejection. Existing tests mostly start from the populated example. | A designer cannot follow the documented stage order while keeping drafts valid and resuming via status. | Fix first under WP-01 / ADR-001; keep coverage enforcement at execution and explicit strict validation. |
| F-02 / high | No observed complete beginner/existing-guidelines/AI-experience agent sessions, no no-skill/old-skill comparison, and no learner observations. This session's available-skills catalog now lists six Fievel skills, which is limited discovery evidence, not behavioral acceptance. | The central teach/build promise is untested despite the CLI suite passing. | WP-02; seed cases and fresh-context protocol. Do not claim end-to-end usability. |
| F-03 / high | Human review sheets include questions and responses but no scenario/context snapshot, rule text, source evidence or pass/fail/borderline rubric. They have no completed-review schema or validation. | Reviewers need the mutable current package; meaning and consistent judgment are underspecified. A hash detects difference but cannot reconstruct old evidence. | WP-03; design the evidence/rubric contract before implementation. |
| F-04 / medium | An all-human definition yields deterministic_execution with zero passes/failures and all checks not_run. Current CLI exits 0 whenever literal failures are zero. Missing response situations also stay not_run. The behavior is documented, but executed coverage is not prominent. | “Command succeeded” is easy to confuse with “quality checked”; a report does not state a useful readiness verdict. | WP-04; define execution coverage and status vocabulary, preserving the distinction from overall quality. |
| F-05 / medium | sync --check compares expected files only. A stale extra Claude skill is invisible to it; the isolated adapter probe still reports eight successful checks. No ownership manifest identifies deletable generated files. | Retired guidance can remain discoverable after skill renames/removal. | WP-05; never solve this by deleting every unexpected user skill. |
| F-06 / medium | Example initialization copies seven drafted stages and a results-first next_action. The novice receives the completed reference package rather than constructing it. responses-good.json deliberately contains a bad factual claim. | Learners can mistake reference state for their progress and fixture naming for a quality judgment. | WP-06; distinguish practice entry from reference artifacts; preserve original evidence. |
| F-07 / medium | Four short introductory modules do not cover the brief's educational scope. Registry categories exist, but rules do not cite exact source passages or approval evidence; authority and freshness are declared metadata. | The differentiating teaching/source-quality experience is a skeleton. | WP-07 and phase E/H. Expand based on learning goals and observations, not folder count. |
| F-08 / medium | Original research uses broad summaries; metadata has no pinned revision. Several decisions lack alternatives and falsification criteria. Files are not yet in Git history; transitive dependencies are unlocked; CI is configured but not run remotely. | Harder to review changes, reproduce assumptions and maintain claims over time. | Deepened source inspection, baseline, decision and iteration records now; dependency/CI/history work remains explicit. |

Priorities reflect impact on the first learning workflow, not security severity.

## What remains useful

Keep the no-overwrite initialization/report behavior, separation of definitions and
execution, human questions left pending, stable rule/check IDs, JSON Schema reuse,
fictional exercise and honest platform caveats. Their existence is useful evidence
for local functionality, not sufficient evidence for the product's educational goal.

## Assessment

The first pass is an executable foundation with draft workflows. It should not be
treated as an accepted functional release of the guided experience. The next work
is evidence-led: repair the demonstrated stage-order defect, observe real agent
journeys, and make human review usable before adding optional model integrations.

Status updates belong in ../../ITERATIONS.md and ../../REQUIREMENTS.md; this file
preserves what was observed before remediation. Findings remain open until their
stated acceptance evidence exists.
