# Research round 2: turn references into testable decisions

Date: 2026-10-21. Question: which upstream mechanisms help Fievel teach, build and
evaluate reliably, and what would demonstrate that they help? This extends the
initial comparison in ../RESEARCH.md. It does not claim any upstream runtime was run.

## Method and limits

Inspected selected upstream skill/evaluation source files at pinned revisions,
primary tool documentation and focused design-system patterns. Exact inspected
paths, revisions and content hashes are in
[upstream-inspection.json](../audits/2026-10-21/upstream-inspection.json).
Full upstream files were read locally under ignored .scratch for inspection, not
vendored into Fievel. We inspected relevant sections, not every line or every
upstream component. Repository status/license metadata alone is insufficient.

Evidence labels in this document: **Observation** is what a source describes or a
file contains. **Inference** is our interpretation for Fievel. **Decision** is a
bounded project choice. **Experiment** states how to test the choice.

## R2-01: Evaluate Fievel itself, separately from systems it produces

Observation: Microsoft's eval-guide includes a
[plan for evaluating the skill itself](https://github.com/microsoft/eval-guide/blob/7a22a8957ced79a35fd7b4634fd5b5eac56c308e/evals/eval-plan.md)
and [behavior cases](https://github.com/microsoft/eval-guide/blob/7a22a8957ced79a35fd7b4634fd5b5eac56c308e/evals/test-cases.json),
including activation and planning outcomes. Its
[playbook](https://github.com/microsoft/eval-guide/blob/7a22a8957ced79a35fd7b4634fd5b5eac56c308e/skills/eval-guide/playbook.md)
separates methodology, session workflow and maturity assessment.

Inference: Fievel's Python tests and booking examples evaluate different targets
from its teaching and authoring behavior. Decision: create a small separate
behavioral suite. Do not import upstream platform-specific thresholds, workbook
contracts, numerical heuristics or maturity claims as universal facts.
Experiment: three fresh-context anchor journeys, compared with the preserved prior
guidance; inspect actual output and failure reasons before expanding the suite.
Links: F-02; FR-02/04/11; phase C.

## R2-02: Choose the method for the failure, and make judgment evidence visible

Observation: the scenario library's
[method-selection guide](https://github.com/microsoft/ai-agent-eval-scenario-library/blob/04fc731937cd2bb8b9ef5195540c6f53914f52a5/resources/evaluation-method-selection-guide.md)
distinguishes textual, meaning, capability and quality checks. Its
[grounding scenarios](https://github.com/microsoft/ai-agent-eval-scenario-library/blob/04fc731937cd2bb8b9ef5195540c6f53914f52a5/capability-scenarios/knowledge-grounding-and-accuracy.md)
include missing/conflicting sources; [failure scenarios](https://github.com/microsoft/ai-agent-eval-scenario-library/blob/04fc731937cd2bb8b9ef5195540c6f53914f52a5/capability-scenarios/graceful-failure-and-escalation.md)
address limits and recovery. These are platform-oriented examples, not verified
policies for Fievel or every agent.

Inference: a yes/no question and a hash are insufficient for independent review.
Decision: specify a review contract containing situation/context, source locators,
rule text, pass/fail/borderline guidance and response origin before implementing a
review validator. Never infer actual tool use from a claim in response text.
Experiment: use intentionally correct, incorrect and ambiguous answers; ask two
reviewers to justify judgments using only the saved review package. Analyze
disagreement before choosing a scoring threshold. Links: F-03/04; WP-03/04.

## R2-03: Test skill improvements against a baseline in clean contexts

Observation: [Agent Skills evaluation guidance](https://agentskills.io/skill-creation/evaluating-skills)
describes realistic prompts, clean contexts, baseline comparisons and iteration
artifacts. Format compliance alone does not establish usefulness.

Inference: this authoring conversation is contaminated as an evaluation context:
it already knows the intended behavior and implementation. Decision: distinguish
self-inspection from fresh-session observations and user research. Begin with a
small set and expand after actual failures. No separate agents were launched in
this review. Experiment: repeat the same entry/resume prompts with old/new skill
guidance, record host/model and all setup differences; do not call this causal
evidence if model or context also changes. Links: F-02; validation strategy.

## R2-04: Reconsider the reason for deferring Promptfoo

Observation: Promptfoo's [echo provider](https://www.promptfoo.dev/docs/providers/echo/)
can run assertions on existing outputs without a new model call. Its
[manual-input provider](https://www.promptfoo.dev/docs/providers/manual-input/)
accepts typed responses. Echo does not make model-graded assertions free of network
or cost; grader/embedding providers can still be called.

Correction to the first pass: “we need a paid/live target first” is too broad a
reason to defer all Promptfoo validation. Saved outputs are already a testable target.
Decision: schedule a pinned, offline echo spike before writing a production adapter.
Keep the small local CLI as a baseline; do not assume dependency weight justifies
custom implementations indefinitely. Experiment: compare the three existing literal
checks against the same saved outputs, with no model-graded assertions; document
setup/runtime, case/substring semantics, output provenance and any network behavior.
No Promptfoo binary or integration has been run in this review. Links: phase F.

## R2-05: Vale is a specific terminology reuse candidate

Observation: Vale's [substitution rule documentation](https://docs.vale.sh/checks/substitution)
describes preferred replacements, case options and word boundaries. Fievel's
not_contains check searches substrings and does not supply term replacements.
Decision: evaluate approved-term export in a separate spike, rather than extending
literal checks into a prose engine. Experiment: booking/ticket, plural forms,
capitalization, substrings and conflicting term mappings against a pinned binary.
Do not claim an exported rule works until actual Vale output is inspected.
No binary run yet. Links: phase F; EX-06.

## R2-06: Separate visible progress from proof of learning

Observation: GOV.UK's [multiple-task pattern](https://design-system.service.gov.uk/patterns/complete-multiple-tasks/)
explains task/order/completion visibility; its
[question-page guidance](https://design-system.service.gov.uk/patterns/question-pages/)
supports focused questions and appropriate supporting content. These are web
patterns, not direct validation of an agent conversation.

Inference: a useful progress display should let a learner stop and resume without
forcing later-stage work. Decision: fix the demonstrated draft/coverage conflict
first and keep stage labels explicit. Do not create a dashboard or force a long
questionnaire. Experiment: intermediate-stage save/status/reopen, then observe
actual users deciding what to do next. Links: F-01/06; WP-01/06.

## R2-07: Accessibility and source permissions need more than metadata

Observation: [Carbon's content hub](https://www.carbondesignsystem.com/building-blocks/foundations/content)
routes writers to decision-specific standards and accessibility topics. The
[MCP security guide](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)
addresses concrete authorization/integration risks. Neither establishes that a
source's self-declared permission is trustworthy.

Decision: plan an accessibility learning objective and a source-boundary experiment;
do not add an external connector to make the inventory look functional. Experiment:
one local source with unknown date/owner, one conflict, one restricted document,
and one embedded instruction attempting to override Fievel. Review response and
files for actual scope/provenance handling. Links: SRC-01; EX-04/05/07; phase E.

## License precision and corrections

The initial matrix used the Agent Skills repository's Apache-2.0 declaration.
The inspected [docs/LICENSE](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/LICENSE)
identifies **CC BY 4.0** for its documentation, a distinct reuse scope. GOV.UK's
[patterns page](https://design-system.service.gov.uk/patterns/) identifies **OGL v3.0**
for site content except where stated otherwise; the code repository's MIT license
does not replace that. We reference and summarize these resources, not copy their
implementation or relicense their content. Any future copied/adapted material needs
file-level license review and attribution. Code, documentation and style packages
can have different licenses within the same project.

## Open research questions

| ID | Question | Next useful evidence |
|---|---|---|
| Q-01 | Does JSON help portability enough to justify novice editing friction? | Observe a learner revise a rule and recover from a validation error; compare agent-assisted Markdown + structured export if needed |
| Q-02 | Are six skills the right discovery surface? | Actual routing errors and task completion, compared with fewer entry points; no restructuring until observed |
| Q-03 | What is a useful human rubric for “does not invent policy”? | Source-bound known/borderline/unsupported examples and reviewer disagreement |
| Q-04 | Does the fictional example teach construction or just inspection? | Compare practice-start and completed-reference journeys with learners |
| Q-05 | Which target host should be called supported first? | Fresh-session Codex exercise, then independent Claude/VS Code trials; one host passing cannot imply all |
| Q-06 | How much evaluation automation benefits the first user task? | Promptfoo/Vale spikes and learner burden, rather than feature parity with upstream tools |

These questions remain open. The new documentation makes them testable; it does
not resolve them by assertion. See ../ITERATIONS.md for actual work completed.
