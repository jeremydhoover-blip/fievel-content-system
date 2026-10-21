> Updated decision, 2026-10-21: Jeremy authorized model calls and changed the sequence to focused repository readiness → local Codex plugin → fresh-session automated trials → Jeremy's hands-on trial → fixes. Broader comparative research remains necessary for public value claims, but no longer blocks the pilot plugin. Earlier no-model and plugin-deferral statements below are historical and superseded by this decision. No external publication or participant outreach is authorized.

# Repository first, plugins second

Date: 2026-10-21. Status: working plan requested by Jeremy. Gates below are proposed acceptance criteria, not completed results.

## Outcome

Release a free repository that helps a content designer turn guidance into a usable content system, apply it to an AI experience, evaluate actual responses, and keep improving it. Begin plugin implementation only after the repository demonstrates both reliable operation and a meaningful benefit over existing workflows.

We cannot prove that no comparable product exists. We can identify relevant alternatives, demonstrate a specific advantage in matched tasks, and make a claim bounded by that evidence.

## Product hypothesis

For a content designer working on an AI experience, Fievel makes it easier to connect source guidance, content standards, AI behavior, quality checks, and review evidence in a portable system they understand and own.

The proposed first test scenario is an AI support experience with fictional product policies and writing guidance. Test both building the system and changing a policy later. Files, skills, brand rules, and evaluation tools alone are not the differentiation. The hypothesis is that the connected, guided workflow reduces omissions and maintenance effort while preserving source fidelity and user control.

## Starting evidence

The I29 development record reports 82 passing tests and eight matching generated adapters. That is historical software evidence, not a new run or proof of agent behavior. Source provenance checks, consumer exports, saved-response checking, human-review contracts, and an offline viewer are implemented.

- FB-01, FB-02, and FB-03 are prepared but NOT RUN: beginner, existing guidelines, and resume.
- Human calibration packets exist; judgments remain pending.
- The isolated setup exercise reused local dependencies after offline installation failed. A clean dependency installation is not demonstrated.
- Generated adapters do not establish successful operation in each host.
- Consumer export does not prove that a consuming AI follows the system.

References: [iterations](ITERATIONS.md), [prepared trials](../evals/fievel-behavior/prepared-2026-10-21/README.md), [calibration](../evals/human-review-calibration/round-01/README.md), [requirements](REQUIREMENTS.md).

## Sequence and acceptance gates

| Phase | Work | Evidence needed to advance |
| --- | --- | --- |
| 1. Establish the release baseline | Reconcile requirements, current features, known gaps, and landing-page promises. Record candidate revision or file manifest, dependencies, supported environments, and exact commands. | One acceptance ledger linking each material claim to evidence or an explicit unverified status; no stale historical gate presented as current. |
| 2. Prove repository operation | Exercise clean setup and the full local lifecycle: initialize, draft, validate, provenance, coverage, saved-response checks, human review, export, viewer, and resume. Include malformed inputs, missing responses, conflicting sources, stale evidence, existing-file protection, and recovery. | Reproducible command transcripts and artifacts on every environment claimed as supported. Required core tests and adapter sync pass after core fixes. Unsupported environments are clearly labeled. |
| 3. Prove actual agent behavior | Run the three frozen behavioral trials in fresh sessions. Test discovery and activation in each claimed host. Add an end-to-end consuming-AI trial using a reviewed system and saved outputs. | Assessed transcripts and artifacts show faithful rules, preserved unknowns, usable outputs, and correct draft/approval/execution boundaries. Any critical failure is fixed and its case rerun. |
| 4. Demonstrate added value | Compare Fievel with a competent plain-agent-plus-guidelines workflow, then the closest relevant tool workflow. Run a source-change and resume exercise as well as initial creation. | Independent assessments show a concrete user benefit without loss of fidelity. Report failures, ties, setup burden, and limits as prominently as wins. |
| 5. Prepare the free release | Fix observed blockers, simplify first use, document troubleshooting and support limits, verify licensing/attribution and example data, align public promises with evidence. | Written release decision with no unresolved critical failures and evidence for every advertised core journey. Jeremy accepts the bounded product positioning. |
| 6. Package plugins | Choose the first host from observed demand and installation friction. Package the proven shared core; test installation, activation, updates, removal, permissions, and project preservation. | A separate plugin plan after the repository gate passes. Distribution packaging and store acceptance are separate from product validation. |

Phases 1–2 can advance without model calls, using local fixtures and saved responses. A genuinely clean dependency install may require separately authorized downloads. Phases 3–4 require separately authorized model usage and actual human participation; the earlier no-model-calls constraint remains in force. Do not contact participants or run those trials merely because this plan exists.

## What “end to end” must cover

1. A new user installs the documented prerequisites and starts Fievel without developer coaching.
2. They bring approved fictional guidance, identify source authority and unresolved questions, and create draft standards and behavior rules.
3. They understand what is draft, what they approved, and what is still missing. Structural validation never substitutes for approval.
4. They export the reviewed system and use it in a consuming AI task. Save the actual response and its origin.
5. They run applicable literal checks and complete human judgments. Missing responses and pending judgments remain visible.
6. They use the evidence to revise the system, change a source policy, identify affected rules/checks, and reassess outputs. Manual impact tracing must be labeled manual unless automation exists.
7. They resume in a fresh session without losing decisions, source links, or unrelated files, and inspect a newly generated viewer snapshot.

## Value experiment

Before execution, freeze the tasks, source pack, rubric, time budget, model/host configuration, and meaningful-benefit threshold. Avoid selecting a threshold after seeing results.

- Baseline A: the same capable coding agent, the same guidelines, and a competent task prompt, without Fievel.
- Baseline B: the closest practical existing workflow from the [market scan](research/ROUND-05-PRODUCT-VALUE.md). Record unavailable access as untested, not a feature absence.
- Candidate: the frozen Fievel release candidate with equal input and comparable assistance/model budget.
- Assess source fidelity, missing requirements, usefulness of rules/checks, understanding of approval/results, time and help required, and effort to update after a source change.
- Use independent human assessment where judgment is required. Blind output identities where practical; balance task order and use equivalent scenarios to reduce learning effects.
- Start with the existing proposal of three beginners and two experienced designers. Treat this as qualitative discovery, not statistical proof. Record who benefits and who does not.

Proposed product gate: at least four of five participants complete the core journey without developer intervention, and at least three show a predefined meaningful improvement over baseline in completeness or maintenance effort without reduced source fidelity. Any fabricated policy, false approval/pass claim, or unintended data loss blocks advancement until resolved. Confirm these thresholds before recruiting; a small pilot supports only a narrow claim.

If the benefit is unclear, improve or narrow the workflow and repeat the comparison before building plugins. Plugins should remove demonstrated adoption friction, not conceal an unproven product.

## Immediate action register

| ID | Next deliverable | Requirement/finding links | Dependency / owner |
| --- | --- | --- | --- |
| RP-01 | Current claim-to-evidence ledger and prioritized gap list | EX-06, FR-12, F-08 | First; engineering agent drafts, Jeremy reviews positioning |
| RP-02 | Clean-install and deterministic lifecycle evidence on the candidate | TR-06–08, FR-10–11, PORT-01 | RP-01; engineering agent; downloads only when authorized |
| RP-03 | Fix and verify measured repository blockers | Relevant failing requirement, F-01–05 | RP-02; engineering agent |
| RP-04 | Frozen host/behavior/consumer trial protocol and eventual results | FR-01–03, SYS-01–02, F-02 | RP-03; execution waits for model authorization |
| RP-05 | Completed independent human calibration and usability/value study | FR-12, EX-01–04, UX-01–02 | Jeremy arranges participants; no outreach authorized |
| RP-06 | Source-change/resume evidence and release decision | GOV-01, SRC-01, TR-10, EX-05 | RP-04–05; engineering agent compiles, Jeremy decides |
| RP-07 | First plugin scope grounded in observed friction | PORT-01, TR-08 | Only after RP-06 passes |

Dates remain unscheduled. The next authorized development step is RP-01, followed by local deterministic verification and fixes. This document does not authorize model calls, external publication, participant outreach, or plugin implementation.
