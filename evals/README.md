# Evaluation evidence

The definitions are in examples/wayfarer/evaluation.json. Files in evidence/ were
produced by actual CLI executions on 2026-10-21 against authored response fixtures.
They are not live AI response evaluations or completed human reviews.

| Evidence | Actual outcome |
|---|---|
| literal-pass.json | 3 literal passes, 0 literal failures, 6 human questions not run |
| literal-fail.json | 0 literal passes, 3 literal failures, 6 human questions not run |
| pending-human-review.json | 6 pending human questions; no reviewer or judgments claimed |

The reports include copied responses and hashes for reproducibility. The
literal-pass fixture deliberately includes an invented refund time; see
examples/wayfarer/conversations.md. Literal passes do not establish overall quality.

Generate a new report rather than overwrite these files. The CLI returns 0 for no
literal failures, 1 for literal failures, and 2 for invalid inputs or file errors.
An exit code of 0 can include not_run checks and is not a release-quality verdict.
