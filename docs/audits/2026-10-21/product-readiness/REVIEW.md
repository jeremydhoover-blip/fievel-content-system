# Product readiness review

Date: 2026-10-21
Scope: landing-page promises, core CLI, package validation, reports, viewer and
existing guided-authoring evidence. Implementation-agent self-audit, not independent
product acceptance. UI direction accepted by the user; no visual redesign in scope.

## Assessment

The local deterministic foundation works in exercised paths. Fievel is not yet
verified end to end as a guided content-system product. There is no server backend:
Python and local JSON files provide persistence, validation and saved-response
checks; the coding agent provides authoring and guidance. Adding a hosted service
would not establish that guidance or consumer behavior works.

## Promise to evidence

| Promise | Current evidence | Gap and next gate |
|---|---|---|
| Build from product context | Blank/example initialization and structural validation executed successfully | FB-01 must create a different product from actual user turns without inventing policy |
| Turn existing guidance into standards | Structured rules and declared source IDs work | FR-06, SYS-01, SRC-01: actual conversion fidelity, evidence locators, conflicts and authority need execution and review |
| Define AI behavior | Behavior schema and linked rules validate | FR-07: no-tool, clarification and uncertainty decisions need observed authoring and consumer behavior |
| Quality checks | Literal fixture produced 3 pass and 6 not_run; all-human fixture produced 0 executed | FR-09, F-03/04: literal checks are narrow; human judgment remains pending and lacks a self-contained evidence/rubric contract |
| View connections | Real package plus generated report exported successfully; 12 viewer unit tests pass | Declared links are not verified grounding; viewer is an offline snapshot |
| Resume work | Progress structure and partial-draft tests pass | FR-11: FB-03 needs fresh-context continuity with sentinel preservation |
| Agent portability | Eight generated adapters match canonical sources | FR-01/02, PORT-01: clean activation and host-specific behavior are unverified |
| Maintain safely | Overwrite attempt rejected; hashes and links tested | F-05: stale extra generated skills are not detected; lifecycle ownership needs a manifest design |

## Executed evidence

- Baseline: 35 tests passed and eight adapter checks passed.
- Fresh disposable CLI exercise: blank and example init, validate, status,
  literal check, pending review and viewer-with-report succeeded. Report overwrite
  failed as expected. See probes.json. Disposable packages removed after probes.
- The first all-human probe used an invalid null value and correctly failed schema
  validation. Preserve that failure; all-human-corrected.json records the valid
  string-value fixture: exit 0 with 0 pass, 0 fail, 9 not_run.
- No behavioral case, model generation, completed human review, learner session,
  external source ingestion or remote CI was executed in this increment.

## First repair

F-04 / TR-03 / WP-04: make execution coverage visible in CLI output. Two new
regression tests failed before implementation, then the full 37-test suite passed.
The CLI now prints executed/defined counts, checks missing supplied responses,
and checks awaiting human review. It explicitly says when no automated checks ran
and that this is not an overall quality verdict. Existing exit codes and saved
report shape remain compatible. Missing-response checks and human-review checks
are counted separately without double counting. This is a bounded reporting repair,
not completion of the review contract or overall WP-04 acceptance.

## Prioritized next work

1. WP-02 / F-02: execute FB-01, FB-02 and FB-03 in clean agent contexts. Preserve
   prompts, outputs, changed files and host metadata. Passing means correct routing,
   actual persisted artifacts, unknown policy remaining unknown, and safe resume.
   Current authoring chat cannot substitute for those fresh sessions.
2. WP-03 / F-03: design and version self-contained review packages containing
   scenario, rule and available source context, evidence requirements and rubric.
   Validate completed judgments, reviewer identity and matching hashes. Design a
   migration path before changing report contracts. Human calibration needs people.
3. SYS-01/02 and SRC-01: exercise fictional guideline conversion with exact locators,
   conflicts, missing approval and injected source text; then supply a reviewed
   instruction package to a named consumer and test its actual responses.
4. WP-05: define generated-adapter ownership and stale detection while preserving
   unrelated skills. Test removed/renamed canonical skills in a disposable copy.
5. Clean setup and host activation, then real designer sessions. Keep independent
   accessibility, source review and learner understanding separate from unit tests.

Do not introduce model providers, retrieval services or external connectors simply
to make the backend larger. Select integrations only when an observed user task
requires them. No deployment or external access is part of this increment.

## Current next action

Prepare and execute the three anchor behavioral journeys in genuinely fresh
contexts before claiming the central guided-authoring promise is verified.
The immediate deterministic reporting repair is complete; product acceptance is open.
