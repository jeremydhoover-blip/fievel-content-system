---
name: evaluation-designer
description: Create plain-language Fievel quality checks, check saved responses, or prepare human review without claiming unexecuted tests ran.
---

# Evaluation Designer

Read AGENTS.md and stages 5–6 of docs/WORKFLOW.md. Required inputs: actual design
requirements, realistic user situations and a project folder. Read
knowledge/evaluations/checking-quality.md on demand. Translate “good” into inspectable
questions; link each check's requirement_id to a standards or behavior rule.
Cover ordinary, unknown, conflicting-source and action-request situations.

Use contains/not_contains only for case-insensitive literal checks. Use human for
meaning, invented facts, tone, accessibility and action authorization. A phrase
absence cannot prove the absence of unauthorized action. Store definitions in
evaluation.json. Drafts can be saved before coverage is complete; before execution,
run `python scripts/fievel.py validate <folder> --require-coverage` and address
uncovered requirements. With no saved responses, explain that checks are defined,
not run.

To inspect a real saved execution report alongside the package, generate
`python scripts/fievel.py view <folder> --report <execution.json> --out <new.html>`.
The viewer reproduces literal outcomes before presenting totals, and marks stale,
unsupported or altered reports. It does not validate completed human judgments
or establish the origin of saved responses. Do not equate reproduced with approved.

With actual saved text mapped by scenario ID, run:
`python scripts/fievel.py check <folder> --responses <json> --out <new-report.json>`.
Prepare a separate review using `review` with the same arguments. Human questions
stay not_run in execution and pending in the review sheet. The reviewer records
identity, date, pass/fail and rationale; never fabricate completed human judgments.
For a self-contained evidence review, read docs/HUMAN-REVIEW.md. Use
`review <folder> --responses <json> --evidence-config <config> --out <new.json>`.
The configuration supplies draft/reviewed rubrics, explicit source excerpts and
response origins; never invent approved criteria or fetch source locations implicitly.
`validate-review <report> --require-complete` checks completed records; add
`--folder <folder>` to reject staleness. Missing responses remain not_run; pending,
borderline and insufficient_evidence cannot count as complete. A complete record
can contain failures and is not content approval or authenticated human authorship.
Legacy sheets must be regenerated in the opt-in format rather than relabeled.

AI judgments, if requested conversationally, must be labeled AI suggestions and
stored separately; no judge backend is implemented.

Output: definitions, actual report if executed, pending review, suggested improvements
in a separate Markdown note. Compare hashes before reusing results after edits.
Recovery: no responses or unknown IDs -> repair the mapping, never substitute fixtures
as evidence about a live agent. Example: “Don’t invent decline reasons” -> human check.
