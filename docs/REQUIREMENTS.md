# Requirements and acceptance evidence

Source: [the original brief](PRODUCT-BRIEF.md), especially sections 5–15 and 18,
plus the user's request for deliberate research, planning and iterative validation.
Reviewed 2026-10-21. These are acceptance claims, not a list of files to create.

Evidence levels: **A** authored guidance/artifact; **S** static inspection;
**X** executed script/automated check; **B** observed agent behavior in a recorded
host session; **U** observed intended-user outcome. A requirement may need multiple
levels. A file existing proves A, not B or U. “Partial” means some evidence exists
but the acceptance condition remains open. No row is fully product-accepted yet.

## Functional acceptance from the brief

| ID | User outcome | Present evidence / state | Evidence still needed | Work |
|---|---|---|---|---|
| FR-01 | Open the repository in a supported agent environment | Current Codex workspace exists; adapters inspected (S); partial | Record independent host/version and fresh open/activation | Phase G |
| FR-02 | Activate Fievel using documented instructions | Six skills listed in this session's catalog; explicit-read prompt documented (S); partial | Fresh-context skill invocation and observed routing (B) | WP-02 |
| FR-03 | Choose beginner or existing-project path | Paths in guidance/schema (A/S); partial | Observed choice handling for all three entry paths (B) | WP-02 |
| FR-04 | Receive guidance suited to experience | Guided/brief preference exists (A); partial | Beginner explanations and expert skipping observed; learner comprehension (B/U) | WP-02, H |
| FR-05 | Define basic product and audience context | Template/example and CLI initialization (X); partial | New product built from user decisions rather than prefilled fiction (B/U) | Phase B/C |
| FR-06 | Create structured content standards | Rules/terms/patterns and WP-01 partial-draft journey tested (X); partial | Existing standards preserved with provenance; observed designer creation (B/U) | WP-01 verified locally; E |
| FR-07 | Define basic AI behavior | Draft example and behavior skill (A/S); partial | Responsibilities/confirmation/uncertainty decisions elicited without invented tools (B) | WP-02, E |
| FR-08 | Produce realistic situations to test | Four authored Wayfarer situations (A/S); partial | Agent generates appropriate situations for another product; content owner reviews realism (B/U) | C/D |
| FR-09 | Identify things to check in responses | Nine linked questions, three literal checks (X); partial | Inspectable human rubrics, plausible borderline cases and judgment consistency | WP-03 |
| FR-10 | Save understandable project files | Actual initialization/check/review files (X); partial | Designer can locate/explain outputs and use them without interpreting internal code (U) | H |
| FR-11 | Resume without relying on chat history | progress persisted; full/partial package status and saved decisions tested (X); partial | Cross-session agent decision continuity (B) | WP-01 verified locally; WP-02, G |
| FR-12 | Understand what was created and how to use it | START-HERE and README (A); partial | Learner explains one source→rule→check relationship and makes a revision (U) | H |

## Technical acceptance

| ID | Requirement | Present evidence / state | Remaining acceptance | Work |
|---|---|---|---|---|
| TR-01 | No mandatory paid API keys for initial experience | No model client/network in CLI (S/X); local path verified | Actual learner completes with an available agent account; accurately state agent access costs | C/H |
| TR-02 | No mandatory external MCP connection | CLI runs without one (X) | Guided workflow behaves correctly without connections (B) | C |
| TR-03 | No unsupported execution claims | Definitions/results separated and human checks not_run (X); partial | Agent descriptions accurate for missing target, all-human and partial runs (B) | WP-02/04 |
| TR-04 | No credentials committed | No real credentials observed in authored files (S); no project commits | Establish tracked-file secret checks/review before public release; not a guarantee about private local files | H |
| TR-05 | No automatic changes to unrelated user files | Init/report overwrite refusal tested (X); partial | Exercise agent edits, custom folder and sync ownership boundaries (B/X) | C, WP-05 |
| TR-06 | Structured outputs validated where schemas provided | Package schema/links and separate draft/coverage gates tested (X); partial | Version execution/review contracts and validate completed judgments | WP-01 verified locally; WP-03 |
| TR-07 | Critical functionality has automated checks | 21-test baseline; 23 tests after partial-stage repair (X) | Additional evidence/adapter/source contracts as implemented; add tests only for actual contracts | D/E |
| TR-08 | Installation and activation steps actually tested | --target install and Windows CLI walkthrough (X); partial | Clean install/host activation, Linux/other Python versions, truthful support matrix | G/H |
| TR-09 | Attribution and license compliance | Upstream license declarations recorded; no upstream implementation copied (S); partial | Correct file-level docs licenses; pin/review any integration before code reuse; dependency notices | Research/F/H |
| TR-10 | Ownership and reusable portable artifacts | Local seven-file package, ignored user directory (A/X); partial | Export/use instructions for a consuming agent; migration policy; learner ownership tested | C/G/H |

## Experience acceptance

| ID | Requirement | Present evidence / state | Remaining acceptance | Work |
|---|---|---|---|---|
| EX-01 | Nontechnical onboarding is understandable | Original copy and paths (A) | Observe language, setup friction and question burden with learners (U) | H |
| EX-02 | Terminology explained in context | Four short modules (A) | Stage-specific explanations and misconception/transfer checks (B/U) | WP-07 |
| EX-03 | Experienced users can skip explanations | Preference field/skill directions (A) | Direct existing-guidelines and behavior-audit route without beginner gate (B/U) | WP-02 |
| EX-04 | Generated guidance differs from approved standards | Rule status field and instructions (X/A) | No invented approvals; missing source/approver remains visible in observed work (B) | C/E |
| EX-05 | Users retain decisions and assets | No-overwrite CLI, local progress/governance (X) | Consent boundaries and scoped edits observed; generated adapter ownership clarified | C, WP-05 |
| EX-06 | Quality checks trace to design requirements | Stable IDs, links and coverage check (X); partial | Each important requirement represented, method actually tests it, human rubric has evidence | WP-01/03 |
| EX-07 | Errors/unsupported integrations explained clearly | CLI messages and documented limitations (A/X) | Recovery in realistic agent/learner sessions; no fake connectors or actions (B/U) | C/E/H |

## Workstreams beyond the initial acceptance list

| ID | Scope from brief | Present state | Deliberate expansion / exit evidence |
|---|---|---|---|
| KB-01 | Content design foundations | One short module | Learning objectives and exercises for principles, structured content, accessibility, localization, governance; primary-source review and learners |
| KB-02 | AI fundamentals | One context/grounding module | Instructions, context/tokens, retrieval, uncertainty, structured outputs, tool calling/MCP and oversight; conceptual accuracy and transfer exercises |
| KB-03 | AI experience design | One behavior module | Clarification, confirmation, recovery, handoffs, personalization, context and dynamic UI; behavior examples and misconception checks |
| KB-04 | Evaluation quality | One checking module | Criteria/method selection, rubric design, human/judge calibration, regression, multi-turn and tool evidence; no claims of unsupported execution |
| SRC-01 | Source authority/provenance/freshness | Metadata and skill guidance | Actual local evidence locators, conflicts, missing sources, permission boundaries and injection cases tested |
| GOV-01 | Maintenance and community | LICENSE/CONTRIBUTING/version/governance templates | Review ownership, decision history, migration policy, contribution checks and clean release evidence |
| PORT-01 | Shared skills/tool-specific adapters | Generated copies; equality check | Native activation, stale-generated detection, scoped preservation and cross-host resume independently tested |
| EVAL-01 | Optional Promptfoo/Vale backends | Documentation research | Bounded offline comparisons with runtime evidence; adopt only if useful to an observed task |

## Experience amendment: UI, guided authoring and local knowledge

Source: the user's latest direction. The companion UI is now part of the intended
repository experience, extending the original graphical-product deferral. These
requirements remain proposed acceptance criteria, not completed implementation.

| ID | User outcome / constraint | Current evidence | Acceptance still needed |
|---|---|---|---|
| UI-01 | Pleasant high-level view of the content system | Real-file overview snapshot implemented; browser checks (X) | Designer comprehension/usefulness; clear larger-package navigation (U) |
| UI-02 | Trace how sources, rules and checks connect | Actual IDs drive linear source/rule/check trail; missing/ambiguous refs tested (X) | Designer can locate evidence and explain a connection; recorded links remain weaker than verified grounding |
| UI-03 | Viewer supports the ongoing guided process | Actual next action/decisions and saved stage labels shown; skill routing added (X/A) | Observe first-use/resume sessions and user understanding of recorded completion |
| UI-04 | Files remain authoritative; viewing works locally | Exclusive new output; preserved inputs; unsafe-text/report/network browser tests (X) | Observe refresh/sharing understanding; broader platform/file-size testing |
| UI-05 | Connections are accessible without spatial manipulation | Normal controls/linear trail; basic keyboard and narrow-width checks (X) | Independent screen-reader/contrast/conformance evaluation and intended-user tasks |
| UX-01 | Distinctive, focused first-use experience | Journey specification; existing skill skeleton | New user creates/understands a useful artifact without long questionnaire or mandatory connector |
| UX-02 | Expert and returning users retain momentum | Brief route/saved-state model | Real guideline conversion and resume sessions; no redundant onboarding; scoped changes |
| SYS-01 | Existing standards represented faithfully | New local procedure; skill routing (A) | Source locators, authority/context and interpretation assessed against supplied material |
| SYS-02 | System can be deliberately integrated into a consuming AI experience | New explanation distinguishes instructions, skills, sources and schema (A) | Reviewed consumer contract/composition and actual response/tool checks; no automatic enforcement claim |
| KB-05 | Routine guidance uses a useful bundled knowledge base | Seven modules, including three expanded draft lessons; task router (A/S) | Accuracy review, successful local routing and learner exercise/teach-back |
| KB-06 | Local education differs from organizational and version-sensitive sources | Knowledge architecture and core instruction amendment (A) | Agent doesn't substitute lessons for policy; offline concepts work; current tool claims are verified when needed |

## Updating this matrix

Link results to dated evidence, not just a test count. Record whether the issue is
in Fievel, a source, a grader, the exercise or the test itself. Do not silently
lower acceptance criteria to make implementation appear complete. Changed product
requirements need a decision entry and a clear reason. The brief remains the
scope reference; these IDs make it easier to plan and review its implementation.


## I22 evidence update for human review

2026-10-21. FR-09, TR-06 and EX-06 now have executed software evidence for an
opt-in self-contained human-review contract and completed-record validator.
See decisions/ADR-003-human-review-evidence.md and
audits/2026-10-21/review-evidence/RESULTS.md. 48 total tests pass, including eleven
review-evidence tests. No independent human calibration, learner acceptance or
authenticated reviewer identity is claimed. The seven-file package contract and
legacy report formats are unchanged. These requirements remain partially accepted.


## I23 adapter evidence update

TR-05 and PORT-01 have new deterministic evidence for manifest ownership, stale
generated-copy detection and preservation of local/unrelated files. Eight new
fixture tests bring the full suite to 56 passing. See adapter-ownership RESULTS.md
and ADR-004. Historical pre-manifest orphan detection and actual host activation
remain open; this does not close portability acceptance.


## I24 provenance evidence update

SRC-01 and SYS-01 have deterministic evidence for missing metadata, explicit
freshness windows, rule/source evidence links and declared conflict records.
Nine new tests bring the full suite to 65 passing. Refer to ADR-005 and the
source-provenance RESULTS.md. Excerpt accuracy, semantic fidelity, authenticated
authority and human review remain open; no automatic ingestion was introduced.


## I25 malformed input evidence

TR-05/06/07 and EX-07 gained tests for strict JSON, path diagnostics, nesting
limits and report preservation on serialization failure. Full suite: 72 passing;
eight adapters match. See input-hardening RESULTS.md for scope and limits.
No model, learner or clean-install evidence is inferred.


## I26 consumer export evidence

SYS-02/TR-10 have deterministic evidence for a named-consumer review artifact,
exact rule/status selection, separated source data and preserved warnings/conflicts.
78 tests pass; eight adapters match. See ADR-006 and consumer-export RESULTS.md.
No deployment, authenticated approval or actual AI adherence is established.


## I27 setup evidence update

TR-01/02/07/08 and EX-07 gained isolated Windows/Python 3.12.10 runtime evidence
using copied local dependencies. Missing-dependency recovery and the CLI workflow
were exercised; 78 tests passed. Clean offline pip install remains unverified,
with failure preserved. Other platforms and native host activation remain open.
