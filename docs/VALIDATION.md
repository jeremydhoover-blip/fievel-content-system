# Validation evidence — 2026-10-21

This file preserves the first prototype's validation record. The later deliberate
review and WP-01 repair are recorded in [ITERATIONS.md](ITERATIONS.md), with
[before/after logs](audits/2026-10-21/REVIEW.md). The current suite has 23 tests;
the 21-test result below is the earlier baseline, not the complete acceptance case.

After the real-file viewer increment (I-03), **35 tests pass** and browser evidence
is recorded in [viewer experiment results](experience/evidence/viewer-01/RESULTS.md).
The older 21/23-test records remain historical evidence, not current suite totals.

Executed locally on Windows with Python 3.12.10 in the current Codex desktop
engineering session. These checks test real file operations and scripts; they are
not an independent host conversation or automatic skill-discovery test.

## Automated checks

`python -m unittest discover -s tests -v`: **21 tests passed**.

Coverage includes schema validity; template/example packages; new-project creation;
preservation of existing work; malformed fields; unknown and duplicate IDs; broken
source links; uncovered requirements; invalid literal definitions; actual passing
and failing saved-response execution; missing-response handling; pending human
review; evidence hashes; report overwrite refusal; CLI execution from another
working directory; exit codes; adapter equality; skill frontmatter.

`python scripts/fievel.py sync --check`: **8 adapters checked** (six Claude skills
and two instruction adapters). Both bundled packages passed structure/link checks.

The first test attempt exposed an environment restriction on the default temporary
directory. Tests now create temporary projects under the ignored workspace scratch
folder and verify the resolved cleanup path before removing them. A later run
caught a check-count mismatch, corrected before the final passing run.

## README command walkthrough

The documented dependency installation succeeded into .deps with jsonschema 4.26.0.
A virtual environment creation attempt failed at ensurepip in this environment;
the supported --target path avoids that requirement. Initialization created
my-content-system from Wayfarer; status displayed all seven draft stages and the
saved next action. Validation succeeded without marking the package approved.

Actual `check` executions produced [literal-pass](../evals/evidence/literal-pass.json)
(3 pass, 6 not_run) and [literal-fail](../evals/evidence/literal-fail.json)
(3 fail, 6 not_run). The latter correctly returns exit code 1. `review` produced
[six pending human questions](../evals/evidence/pending-human-review.json).
All response text is explicitly authored fictional data. No live target was called.

## Manual inspection and limits

Inspected the product, standards, source inventory, behavior, evaluation definitions,
governance and saved progress. Confirmed each of the five design requirements has
linked checks, all source references resolve, and all example rules remain draft.
Inspected the false refund-time claim to confirm the example demonstrates the
limitations of literal checks. Pending review sheets do not pretend that this
inspection is a completed content-owner review.

No fresh-session Codex activation, Claude Code or VS Code runtime exercise has been
performed. The CI matrix is configured but has not run on GitHub. See
[COMPATIBILITY.md](COMPATIBILITY.md) for the acceptance procedure and remaining work.
