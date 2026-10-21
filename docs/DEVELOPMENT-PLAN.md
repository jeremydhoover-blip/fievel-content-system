> Active pilot sequence (2026-10-21): [Codex plugin pilot](CODEX-PLUGIN-PILOT.md). Model calls are authorized; Jeremy will run the first human trial through the installed plugin. Broader comparative value validation follows the pilot.

> Current priority (2026-10-21): follow [Repository first, plugins second](REPOSITORY-READINESS-PLAN.md). It defines the current release sequence and evidence gates; historical phases below remain background.

# Fievel development plan

Status: active plan, revised 2026-10-21 after reviewing the first prototype.
The product brief is preserved in [PRODUCT-BRIEF.md](PRODUCT-BRIEF.md).
The latest amendment adds a local companion viewing UI and strengthens the
first-use journey, standards integration and bundled knowledge requirements. See
[experience direction](experience/EXPERIENCE-DIRECTION.md) and
[research round 3](research/ROUND-03.md). This updates the original UI deferral;
it does not change the repository-native ownership model.
The user's direction is to proceed methodically: research, record the implications,
plan, implement a bounded change, validate it, and use the result to choose the next
change. File count, elapsed time and passing unit tests are not product acceptance.

## Where we actually are

The first prototype demonstrates file creation, validation and saved-response
substring checks. Its 21-test baseline is reproducible. It has not demonstrated
that a beginner can learn the concepts, complete the seven-stage journey without
assistance, or transfer a working session across agent hosts. Research was initially
mostly README/documentation/metadata review; several architecture choices were
reasonable hypotheses, not conclusions from experiments.

The [audit](audits/2026-10-21/REVIEW.md) records shortcomings without discarding the
prototype. The [requirements matrix](REQUIREMENTS.md) is the acceptance inventory.
[Research round 2](research/ROUND-02.md) links inspected sources to decisions and
experiments. [The validation strategy](VALIDATION-STRATEGY.md) distinguishes what
each kind of evidence can establish.

## Working agreement for each increment

1. Choose one user outcome or failure, using a requirement and finding ID.
2. State the question, current evidence, alternatives and uncertainty before coding.
3. Define the smallest experiment and pass/fail condition. Preserve the baseline.
4. Implement only the change needed to answer that question. Document departures.
5. Run appropriate checks, inspect resulting files and record actual outcomes.
6. Update the decision, requirement state and next action. A failed experiment can
   be useful evidence; it must not be relabeled a completed feature.

The agent can carry out authorized local work without asking for every implementation
choice. Human research needs real participants; owner approval needs the owner.
Neither can be replaced by fictional transcripts or agent self-assessment.
External publication, paid provider use and access to private organizational data
remain separate actions. No such actions are needed for the next local increment.

## Sequence and gates

These are dependency gates, not dates or promises. A phase may contain several
small iterations. Passing a later script check cannot compensate for a failed
earlier user outcome. Optional integration research can proceed independently,
but integrations do not become required to finish the beginner exercise.

| Phase | Question and scope | Deliverables | Evidence to close the gate | Current state |
|---|---|---|---|---|
| A. Establish the baseline | What exists, what was tested, and what did we assume? | Original brief, file hashes, requirement matrix, audit and research ledger | Reproduce baseline, inspect partial workflows, identify material gaps; preserve earlier evidence | Evidence assembled; remediation tracked |
| B. Make drafting coherent | Can a designer create rules before defining checks, stop, and resume? | Validation-boundary decision; staged draft fixture; regression tests | New partial project validates structurally; coverage gaps remain visible; execution still rejects uncovered requirements; broken links still fail | WP-01 local deterministic gate passed; actual agent/learner journey still belongs to C/H |
| C. Test Fievel's guided experience | Does the agent teach/build progressively and adapt to experienced users? | First-use/return journey; small behavioral case set, fresh-context protocol, three path walkthroughs, observed outputs | Start with three anchor cases; compare old/new guidance using identical inputs. Correct routing, saved decisions, local lesson use, no invented policy, no silent overwrites. Expand after first observations | Protocol/seed cases and experience proposal ready; behavioral runs pending |
| C-view. Make the system understandable visually | Can users understand the package and its connections while authoring? | Overview-led local read-only snapshot implemented from actual files | Find next step, trace source→rule→check, distinguish defined/run/reviewed, keyboard/text access, faithful empty/error/stale states | Technical implementation/browser evidence recorded; learner and independent accessibility gates open |
| D. Make checking meaningful | Can a designer judge a response and understand why it failed? | Inspectable rubrics, expected evidence, independently usable review package, completed-review validator | Known pass/fail/borderline responses; saved source/context snapshot; missing evidence rejected; human/AI judgments distinct; grader disagreement analyzed | Design required before implementation |
| E. Support real local guidelines | Can existing standards become traceable rules without losing authority? | Local inventory/ingestion boundary, source excerpts or locators, conflicts/freshness workflow | Unknown authority stays unknown; user decisions preserved; restricted/injected source text cannot become instructions; missing files recover clearly | Designed at instruction level only |
| F. Evaluate reuse in practice | Is Promptfoo/Vale worth integrating for the next real task? | Separate pinned, disposable spikes and decision records | Offline Promptfoo echo can compare known outputs; Vale distinguishes a term from a substring. Record runtime/setup/privacy costs and failed cases | Primary docs inspected; binaries not run |
| G. Verify portability | Can the same learner package resume across hosts? | Host/version matrix, activation evidence, adapter lifecycle rules | Fresh-session discovery, explicit-read fallback, beginner/expert behavior and cross-host resume tested independently | Metadata discovery observed in this session only; other host gates open |
| H. Validate with learners and prepare release | Can intended users do useful work and explain it? | Formative research notes, revised lessons, release checklist, installation evidence | Learners complete and explain the rule→source→check relationship; no unresolved material errors; supported-host evidence matches README claims | Participant testing and release work pending |

Proposed research sample for H: three beginner content designers and two experienced
practitioners for a first formative round, subject to availability and consent.
This is a qualitative diagnostic sample, not evidence of population-level success.
Do not invent a numerical learning-success rate from a handful of sessions.

## Immediate work packages

| ID | Work | Depends on | Acceptance and next decision |
|---|---|---|---|
| WP-01 — locally verified | Separate draft integrity from coverage enforcement (F-01) | Audit probe; ADR-001 | Partial-stage regression passes, strict option still catches omissions, execution unchanged for complete packages. Decide whether a readiness command is needed after seeing real drafting. |
| WP-02 | Run the three anchor behavioral cases (F-02) | WP-01; fresh host context | Save original prompts, host/model/version, artifacts and observed transcript. Separate the evaluator's view from actual learner evidence. Decide which guidance fails before rewriting all six skills. |
| WP-03 | Specify human-review evidence and rubrics (F-03) | Research R2-02; WP-02 observations can inform language | Two reviewers can locate source/context and explain pass/fail/borderline distinctions. Design a versioned review contract and migration plan before changing outputs. |
| WP-04 | Report execution coverage explicitly (F-04) | WP-03 report contract | Zero executed checks, partial responses and all-human checks cannot be mistaken for overall success. Preserve documented CLI compatibility or document a deliberate change. |
| WP-05 | Define stale adapter handling (F-05) | Ownership decision | Drift check surfaces retired generated skills while preserving unrelated user skills. Choose a manifest/marker policy before deleting anything. |
| WP-06 | Repair example naming and learning state (F-06) | Behavioral observation of example entry | Distinct practice-start and completed-reference paths; clearly named literal-pass fixture; earlier reports retained. Avoid fabricating learner progress. |
| WP-07 | Expand curated knowledge deliberately (F-07) | Priority gaps from WP-02/H | Each lesson has learning objective, source evidence, exercise, misconception check and reviewed date. A reviewer checks accuracy; learners test comprehension. |
| WP-08 | Record changes and compatibility (F-08) | All increments | Append iteration outcomes and update requirements. Establish Git history when repository write policy permits; do not claim untracked files are a release. |
| WP-09 — first pass accepted; refinement verified | Prototype and evaluate the local viewer (UI-01–05) | Experience amendment; ADR-002 | Generates a snapshot from actual files; heuristic refinement and browser/diagnostic checks recorded in I-04. Designer tasks, independent accessibility and usefulness evidence still pending. |
| WP-10 | Design first-use and return journeys (UX-01/02) | WP-02 seed cases; viewer proposal | Beginner produces and explains a small artifact; expert starts from provided standards; return session preserves decisions and exposes meaningful next action. |
| WP-11 | Build the local curriculum path (KB-05/06) | Knowledge architecture; observed gaps | Task-based router, focused modules with examples/exercises/criteria and provenance; core explanation/exercise needs no web request. Independent content/learner review still required. |
| WP-12 | Define standards fidelity and consumer instructions (SYS-01/02) | Source locator/approval proposal; relevant local lessons | Exact source→rule mapping inspected; interpretation stays draft; a named consumer receives reviewed instructions and actual behavior is tested. JSON files alone are not integration. |

## Architecture decisions under review

Keep repository-native files, no mandatory external connection and progressive
knowledge loading. These follow the brief. Retain JSON/Python provisionally because
they provide a small working base; neither is proven easiest for nontechnical users.
Seven files are a current contract, not an untouchable design. Future changes need
representative beginner/expert data, a migration note and old-package tests.

Do not adopt the upstream platform's workbook, UI dashboard, numerical thresholds
or enterprise risk taxonomy merely because they exist. Use the smallest relevant
pattern and explain the adaptation. See research/ROUND-02.md for actual reuse decisions.

## Change and evidence records

Use [ITERATIONS.md](ITERATIONS.md) for chronology and [decisions](decisions/ADR-001-validation-boundaries.md)
for consequential choices. Add a new dated experiment result rather than silently
rewriting previous evidence. A source reference, definition, experiment, observed
result and approved decision have different statuses. Dates in this plan are review
dates, not proof that every linked source or host has been validated.

Next: WP-01 has local before/after evidence; run WP-02 in a genuinely fresh
agent context. If the context is unavailable, record that limitation and advance
independent rubric/review design without pretending the gate passed.


## Landing page amendment — research and planning, 2026-10-21

WP-13: plan a short public landing page before implementation. The
[research ledger](research/ROUND-04-LANDING-PAGE.md) informs the
[content and design plan](experience/LANDING-PAGE-PLAN.md), requirements LP-01–08.
Scope includes outcome-led positioning, GitHub/clone CTAs, guided-process preview,
included artifacts, embedded evaluations and precise agent compatibility. No page
or media implementation is authorized by this planning increment. Public repo
URL, hosting and compatibility/demo evidence remain explicit pre-launch decisions.


## Viewer scope correction — user direction, 2026-10-21

The companion UI is a visualization dashboard of the content system created in
an external agent. It shows product context, rules, sources and quality-check
connections/results. Guidance, lessons, next actions and progress tracking belong
in the agent experience, not this viewer. This supersedes earlier proposals to
put those workflow features in the dashboard. See
[I-07](ITERATIONS.md).


## WP-13 execution — I-09

The user subsequently authorized landing-page implementation for future GitHub
Pages. The page and manual-only publishing workflow are implemented locally; see
[the iteration](ITERATIONS.md) and [website instructions](../website/README.md).
The corrected repository destination is supplied. Publishing and remote workflow
execution remain pending; the earlier planning-only scope no longer describes
this increment.


## Product functionality focus after UI acceptance

2026-10-21. User requested product-promise verification. See
audits/2026-10-21/product-readiness/REVIEW.md for fresh probes and priorities.
I20 repairs CLI coverage presentation without changing report contracts.
Next: WP-02 fresh-context anchor journeys and WP-03 review evidence design.
Product acceptance remains open; a hosted backend is not required by the local model.


## WP-02 preparation state after I21

Three candidate explicit-read trial bundles are ready and input hashes verified.
See evals/fievel-behavior/prepared-2026-10-21/README.md. The user selected no model
calls, so execution and native discovery remain not_run. Resume fixture validation
used existing dependencies and is not clean-install evidence. Next independent
work is WP-03 self-contained human-review evidence and rubric contract design.


## WP-03 implementation update after I22

The opt-in evidence contract and completed-record validation are implemented
under ADR-003. See HUMAN-REVIEW.md and audits/2026-10-21/review-evidence/RESULTS.md.
Legacy reports are preserved. 48 automated tests and eight adapter checks pass.
Next WP-03 gate is two independent human reviewers using only frozen context,
with recorded disagreement and rubric refinement. This remains distinct from
software completion and from WP-02 fresh agent-session evidence.


## WP-05 ownership update after I23

Manifest-based stale generated-skill detection and conflict preservation are
implemented under ADR-004. See ADAPTER-MAINTENANCE.md and the adapter-ownership
audit evidence. 56 total tests and eight adapter checks pass. Historical orphans
from before manifest migration still require manual review; native host behavior
is untested. Next offline work: source provenance validation.


## SRC-01 metadata evidence after I24

Offline source provenance audit is implemented under ADR-005. See
SOURCE-PROVENANCE.md and audits/2026-10-21/source-provenance/RESULTS.md.
65 automated tests and eight adapter checks pass. This checks supplied metadata
and links; source meaning, original accuracy, approval authority and undisclosed
conflicts remain unverified. Next offline work: malformed-input hardening and
consumer contract design. WP-02 model calls remain unauthorized.


## Offline hardening after I25

Shared input parsing and pre-serialization report creation now have malformed-input
regression coverage. See input-hardening RESULTS.md. 72 tests and eight adapter
checks pass. This is bounded failure-path coverage, not universal input safety.
Next offline work is a consumer export contract, preserving draft status, source
provenance and action boundaries. Actual consuming-agent adherence stays untested.


## Consumer contract after I26

ADR-006 and CONSUMER-EXPORT.md describe the implemented review artifact and
export-consumer command. 78 tests and eight adapter checks pass. This is portable
review material, not consumer activation or verified adherence. Next offline task:
clean-setup checks with locally available dependencies. Actual consumer behavior
and owner composition remain open.


## Setup evidence after I27

OFFLINE-SETUP.md and offline-setup-final RESULTS.md record isolated runtime
verification. All CLI workflows and 78 tests pass after recovery with existing
local dependencies; eight adapters match. Clean pip installation failed offline
because no matching distribution was available. Broader install/platform evidence
remains open. No model or host activation claims.


## WP-03 calibration preparation after I28

Two reviewer packets and organizer-only comparison materials are ready at
evals/human-review-calibration/round-01. Six pending records validate. Independent
human review and disagreement analysis remain not_run. No model calls or downloads.
Next step requires actual participants; do not substitute agent-authored judgments.


## Human-review usability after I29

review-page now exports readable offline forms with JSON download for CLI validation.
82 tests, eight adapters and browser checks pass. All calibration judgments remain
pending. Real reviewer navigation, rubric clarity and independent calibration remain
open; no autosave or in-place HTML persistence is implemented.
