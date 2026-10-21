# Fievel behavioral evaluations

Target: Fievel's guided authoring behavior, distinct from Wayfarer response checks
in ../evidence. cases.json holds three seed **definitions**. No host execution,
transcript, human grading or pass result is claimed by their presence.

Follow ../../docs/VALIDATION-STRATEGY.md. Use separate clean working copies/contexts,
record exact prompts and host versions, preserve baseline/candidate guidance, and
save observed artifacts. Run three anchor cases before generating many variations.
No automated behavioral runner is implemented yet.

The guidelines fixture is fictional. Its stated authority belongs only to the
controlled test setup; it grants no real organizational approval or external access.
The resume case must be prepared from a blank project with the exact stated
partial-state edits, not the completed Wayfarer example.


## Prepared candidate trials

The user selected preparation without model calls.
[Prepared trials](prepared-2026-10-21/README.md) contain frozen candidate workspaces,
exact turn prompts, manifests and assessment sheets for FB-01/02/03.
All behavioral execution statuses remain not_run. Run the read-only integrity
check with `python evals/fievel-behavior/prepared-2026-10-21/verify.py`.
Preparation checks are separate from agent outcomes and clean-install evidence.
