# Validation strategy

Status: proposed acceptance process, first deterministic baseline executed
2026-10-21. It implements the gates in DEVELOPMENT-PLAN.md. Numerical criteria
below are local engineering/observational acceptance conditions, not externally
established measures of learning effectiveness.

## Three different targets

1. **Fievel's software:** file creation, schema/link checks, preserved work,
   report semantics and adapters. Python regression tests provide direct evidence.
2. **Fievel's agent experience:** onboarding, teaching, eliciting decisions,
   preserving authority, saving work and resuming. Requires recorded host sessions.
3. **The user's designed AI experience:** whether a booking/support/etc. assistant
   follows its rules. Requires actual responses or a configured target and methods
   suited to each claim. Authored fixtures test the checking process, not a live AI.

Learner understanding is a fourth outcome measured through observation/interview,
not inferred from any of those test pass counts. Keep results separate.

## Evidence ladder and gates

| Gate | Required evidence | Failure examples | What it cannot establish |
|---|---|---|---|
| V-01 Integrity | Schema and known links valid, no duplicate IDs, no silent overwrites; drafts can be incomplete | Stage-2 draft blocked by stage-5 requirement; changed unrelated file | Accuracy of policy, source authority or learning |
| V-02 Coverage | Each intended requirement maps to an inspectable check; gaps explicit | A question has a valid ID but doesn't test the instruction; inaccessible implicit quality criterion | A covered requirement actually passed |
| V-03 Execution | Real saved responses/target identified; exact definitions, context and input provenance available; executed/not-run clear | Zero checks run presented as success; supplied response origin unknown; old definition used after edit | Correct human or AI judgments |
| V-04 Grader usefulness | Known pass/fail/borderline cases; expected rationale; human disagreement checked; AI judge compared with human labels if introduced | Substring incorrectly treated as proof of truthful answer; rubric rewards plausible inventions | Generalization to untested requests |
| V-05 Agent behavior | Fresh-context transcripts and output packages for anchor cases and regression variants | Invented company rule, repeated onboarding on resume, expert forced through lessons | Real learner comprehension or cross-host reliability without those trials |
| V-06 User outcome | Consented formative learner sessions, observations and explanations in participants' own words | Can copy files but cannot explain/use their relationships; loses control over edits | Population-wide success rate from a small sample |
| V-07 Release claim | Clean setup, supported host evidence, ownership/license review, tracked release state and known limits | README support claims inferred from adapter files; unrun CI reported green | Perpetual correctness after model/source changes |

## Next deterministic experiment: a partial journey

Run the ADR-001 scenario using a new empty project rather than the finished example.
Persist stage-2 rule, decision and next_action; validate/status/reopen; add stage-5
check; run against a real saved string. Test malformed reference and explicit strict
coverage failure too. Keep the baseline test log, regression result and probe output
under docs/audits/2026-10-21. Passing establishes V-01 behavior for that path.

## Fresh-context behavioral experiment

Seed definitions are in ../evals/fievel-behavior/cases.json. They are **not runs**.
Begin with three cases: novice construction, experienced guidelines conversion,
and resume from stage 2. Use a new context for each case and a new disposable project
folder. Do not supply private data or extra coaching beyond the stated case.

For old/new comparison, use the preserved baseline skill/guidance text and candidate
guidance with identical user inputs. Snapshot the selected files in the trial's
working copy; do not edit core instructions between two supposedly identical runs.
An explicit-read test measures adherence after loading; a native-discovery test is
separate. If only explicit-read was tested, do not claim native invocation works.

Record: case ID, condition (baseline/candidate), host and version, model if known,
skill/guidance revision or file hashes, initial files, exact user prompts, transcript,
files changed, command outputs, observations, assessor, method and limitations.
Unknown values stay unknown. Repeat initially three times per condition if runtime
access permits, to expose obvious variation. This is an exploratory sample, not a
statistical reliability estimate. Do not invent results to meet a target run count.

Assess each case against its expected observations and prohibited behavior.
Hard stops for this experiment: silent overwrite, invented source/approval,
fabricated execution or tool access. Other failures become specific revisions,
then rerun the failed case and a relevant regression case. Preserve earlier failures.

The current development session can inspect guidance, but cannot serve as a clean
behavioral baseline. No autonomous new chat, subagent, paid model run or participant
outreach is scheduled by this document. Use a genuinely available host session;
otherwise keep V-05 pending and advance independent work.

## Human-review design experiment

Before coding a completed-review validator, define one source-bound rubric with:
the requirement and rationale; situation and context; authoritative evidence or
known absence; what pass/fail/borderline mean; acceptable variants; response origin;
reviewer identity; judgment/rationale; and what changes invalidate that judgment.
Use an unambiguously grounded response, an invented claim and a borderline answer.
The existing literal-pass fixture contains an unsupported refund claim and is a
useful negative semantic example, not a successful assistant response.

Have two reviewers assess independently using the saved package only. Record
disagreement and unclear criteria before deciding whether the rubric is useful.
Agent-authored provisional judgments can debug the rubric, but do not replace
independent human labels or become completed human-review evidence.

## Formative learner research

Proposed first round: three beginners and two experienced practitioners, with
consent and fictional data. Record existing knowledge, agent/tool familiarity and
accessibility needs that participants choose to share. Run tasks in their normal
environment where possible; avoid teaching the answer during the observed task.

Tasks: describe one product task; create one sourced/draft rule; explain the action
boundary; choose a check method; review a deliberate false claim; revise a rule;
stop and resume. Afterward ask participants to explain how source, rule and check
relate and what “not run” means. Record assistance, confusion, decisions changed,
recovery, perceived control and useful language. Time is diagnostic, not a speed goal.

Use findings to revise lessons and workflow before expanding integrations. Report
who participated and what was observed, not fabricated quotes or a universal pass
rate. No participants have been recruited or tested yet.

## Additional gates for the experience amendment

For UI-01–05, compare overview-led and connection-led designs on the same fictional
example before choosing the default. Browser interaction/layout checks establish
only that the study functions. A real viewer must read the package, derive actual
ID relationships, preserve files, handle unknown/broken/stale states and expose
text/keyboard alternatives. Then observe designers finding next actions, tracing
evidence and explaining defined versus executed versus reviewed checks.

For KB-05/06, test covered conceptual questions using only bundled material, then
separately test absent company policy and current tool questions. The first should
use local guidance; the second must remain unknown without organizational evidence;
the third must not imply stale documentation is current. Expert review and learner
teach-back are still needed for the new lessons. More words do not establish quality.

For SYS-01/02, inspect the source→rule mapping and the proposed consumer instructions
before evaluating actual behavior. Keep the core Fievel skill, designer's rules and
untrusted source text distinguishable. A passing schema test cannot close this gate.

## Change protocol

Each iteration records question, evidence, chosen change, expected observations,
actual outcomes, interpretation, remaining uncertainty and next step in ITERATIONS.md.
Validate new claims at the right level. Do not rerun broad suites repeatedly without
a changed artifact or unresolved concern. Do rerun relevant regression tests after
code/instruction changes. Keep old evidence readable and distinguish old semantics
from current commands when documentation changes.
