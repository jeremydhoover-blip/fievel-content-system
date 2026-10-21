# Iteration log

This is the continuing work record. Distinguish authored plans, executed technical
experiments, observed agent behavior and learner evidence. Preserve failed results;
update conclusions when better evidence arrives. Dates use the project review date.

## I-00 — initial prototype, 2026-10-21

Implemented a repository-native skeleton, six skills, seven-file package, fictional
example and local checking commands. Twenty-one script tests passed. Research was
a focused survey rather than an exhaustive implementation analysis. No fresh agent
journey or intended-user learning outcome was demonstrated. The initial report
was too easy to read as a completed guided slice; treat it as an executable draft.
Original evidence: [VALIDATION.md](VALIDATION.md) and evals/evidence.

## I-01 — deliberate reassessment and first repair, 2026-10-21

### Question

Can we reproduce the foundation, identify gaps against the actual brief, connect
deeper research to decisions, and repair one observed learning-workflow defect
without treating more files as proof of product success?

### Baseline and new evidence

- Preserved the [original brief](PRODUCT-BRIEF.md), hashes for 62 initial files,
  and 14 matching source/guidance copies before changing them. The repository still
  has no recorded project commit; these snapshots are not Git release history.
- Reproduced the 21-test baseline. Added executable partial-state/review/adapter
  probes and recorded [eight findings](audits/2026-10-21/REVIEW.md).
- Inspected selected upstream implementation/evaluation files at recorded revisions;
  added [research round 2](research/ROUND-02.md), identifying what we learned,
  what is an inference, what to try and what remains untested.
- Created [requirements](REQUIREMENTS.md), a [development plan](DEVELOPMENT-PLAN.md)
  and [validation strategy](VALIDATION-STRATEGY.md), plus three unexecuted Fievel
  behavioral case definitions. These are planned tests, not behavioral results.

### WP-01 experiment

Finding F-01: status/validation rejected a legitimate stage-2 draft before the
guide introduced checks at stage 5. [ADR-001](decisions/ADR-001-validation-boundaries.md)
compares the alternatives and records the chosen validation boundary.

Added two regression tests first. Both failed against the existing implementation:
[before-fix log](audits/2026-10-21/wp01-before-fix-tests.txt).
Changed default validate to check structure/links and expose coverage gaps; added
--require-coverage; retained strict coverage in check/review. Updated relevant skills,
shared instructions, user docs and architecture; synchronized generated adapters.

After the code fix, [23 tests passed](audits/2026-10-21/wp01-after-fix-tests.txt).
The added journey actually creates a partial project, saves decisions/next action,
checks status, enforces coverage before execution, adds a linked check, executes
against supplied text and rejects a subsequently broken requirement link.
Final verification and post-fix probes are preserved alongside the other evidence.
Existing bundled execution evidence is preserved; no historical report or user
content-system file was changed.

### Interpretation

WP-01's deterministic acceptance is satisfied: a well-formed incomplete draft can
exist and be inspected without bypassing execution coverage. F-01's demonstrated
software defect is repaired. This does not establish good agent interaction,
learner understanding, complete review quality or cross-platform reliability.
The other seven findings remain open or partially addressed by better records.

### Next iteration

WP-02: execute the three anchor cases in genuinely fresh host contexts; compare
baseline/candidate guidance with identical inputs, recording setup and results.
The current authoring session cannot supply that independent behavioral evidence.
WP-03 rubric/evidence-contract design can progress independently while host access
is arranged. Do not add a production Promptfoo/Vale connector before a separate,
pinned offline spike and a decision based on actual results.

## I-02 — experience, viewer and local knowledge direction, 2026-10-21

### User direction and scope

The user clarified that the experience starts on receiving the repository and
includes a pleasant UI for viewing the created system and its connections.
They also emphasized faithful integration of their own style guides/rules and a
useful bundled knowledge base. This amends the original UI deferral. The
[experience direction](experience/EXPERIENCE-DIRECTION.md) records that change and
connects the conversational journey, viewer and content-system quality.

### Research and concrete work

[Research round 3](research/ROUND-03.md) examines typed system relationships,
graph-library options, accessible text/reading order, task progress and task-based
learning content. No graph framework has been integrated. The
[viewer proposal](experience/VIEWER-DESIGN.md) distinguishes current data fields
from missing evidence/approval/precedence relationships; the design must not invent
edges merely to make a map look complete.

Created two interactive conversation design alternatives: Overview-led and
Connections-led. They use fictional Wayfarer content, not live file loading.
Both expose declared source→rule→check relationships and distinguish definitions
from results. They are design studies, not a viewer implementation or user research.

Added three substantial bundled draft modules: existing-guidelines conversion,
system relationships, and instructions/skills. Each has an objective, practical
example, limitations, exercise/answer criteria and primary references. Updated
the task router, source registry and relevant skills to use local lessons. The
[knowledge architecture](experience/KNOWLEDGE-ARCHITECTURE.md) separates teaching
material, user decisions, organizational evidence and current external references.
Independent content review and learner validation remain pending.

### Checks and interpretation

The design study's local navigation, rule selection, learning view and native
variant carousel passed headless browser interaction checks. Both variants fit
at tested 1024, 736, 360 and 320px viewport widths without horizontal overflow.
Inspected wide, narrow and dark screenshots. Evidence:
[study-01-browser.json](experience/evidence/study-01-browser.json).
The default browser lookup failed in sandbox; installed Edge needed an external
temporary test profile. The successful check used that isolated profile outside
the sandbox. No private browser session or user content was used.

These checks establish interaction/layout behavior for a fictional study only.
They do not establish accessibility conformance, learner value, source fidelity,
offline agent behavior or a working file viewer. Existing core software tests and
adapter sync are checked separately; no new production CLI feature is claimed.

Final I-02 checks: [23 existing core tests passed](experience/evidence/i02-core-tests.txt),
eight adapters matched, project JSON/local Markdown links were valid, all seven
knowledge routes resolved and registry IDs were unique. See
[i02-verification.json](experience/evidence/i02-verification.json). These are static/
software checks, not evidence that an agent or learner used the new material well.

### Next gates

Observe how designers use the two directions to find a next action, trace a rule
and interpret check status. Then implement a small local read-only snapshot
viewer from actual package files, with safe rendering and faithful missing/stale
states. In parallel, test lesson accuracy, existing-guidelines mapping and
first-use/resume behavior. WP-09–12 and UI/UX/SYS/KB amendment IDs track this work.

## I-03 — real-file overview viewer, 2026-10-21

The user selected Overview-led and asked to proceed. WP-09 is now implemented as
a local read-only snapshot command, with boundaries recorded in
[ADR-002](decisions/ADR-002-local-viewer-snapshot.md). Preserved the changed-file
baseline under experience/evidence/viewer-01 before implementation and added
viewer acceptance tests first.

`view <folder> --out <new.html>` now derives overview, saved next action/decisions,
recorded progress, all content/behavior rules, declared source/check connections,
file diagnostics and three local lessons from actual files. It works with valid
partial drafts and shows missing/invalid sections or ambiguous links. Optional
selected execution reports must reproduce before their totals are presented.
All package/report strings render as text; a hash-based CSP blocks external
resources. Existing files are never overwritten and input preservation is tested.
The normal user snapshot was generated with no execution report selected.

Validation: 35 passing automated tests, including 12 viewer tests; seven real-file
browser fixtures and 20 width/view combinations; no observed page/script/CSP errors
or unexpected page network requests. Keyboard selection/focus, special scenario IDs,
unsafe strings, stale/altered report handling, empty drafts and a larger package
were exercised. Evidence and reproducible optional browser scripts are described
in [RESULTS.md](experience/evidence/viewer-01/RESULTS.md).

The first test assertion for CSP inspected escaped HTML incorrectly; it was fixed
to check the decoded value without relaxing CSP. A special-ID rendering concern
was addressed using own-property lookup and exercised in the hostile browser fixture.
Source files were not edited by generation; an earlier generated snapshot was
preserved and a new overview-02.html created in the ignored user project folder.

This closes the local implementation/technical experiment, not the full UX gate.
There is no editing interface, live watcher, automatic consumer integration,
validated human-review contract or independent accessibility/user study. Next:
observe intended designers finding the saved next action, following one rule to
its source/check and interpreting defined versus executed/human-reviewed evidence.

## I-04 — viewer heuristic refinement, 2026-10-21

The user accepted the first functional UI pass and requested stronger design,
heuristics and experience. The [heuristic review](experience/UI-HEURISTIC-REVIEW.md)
records seven findings and their research basis. The actual viewer now prioritizes
next action and open decisions, discloses supporting context, provides searchable
and filtered rule navigation, a Sources view with rule links, browser history and
selected-rule URLs, and clearer snapshot/report language. Typography, spacing,
responsive layouts and keyboard focus were refined. No package schema or saved
content changed.

Validation: 35 Python tests passed; seven browser fixtures and 24 view/width
combinations passed, including search/filter recovery, large lists, source links,
back/forward and direct links. No observed page errors or unexpected network
requests. [Results and screenshots](experience/evidence/ui-02/RESULTS.md) preserve
this evidence separately from the first pass. This is a heuristic refinement and
technical validation; intended-user observation and independent accessibility
review remain open.

## I-05 — landing page research and plan, 2026-10-21

The user requested research/documentation before implementing a short public page.
Reviewed local product/workflow/compatibility/license evidence and six official
platform/design sources. Recorded source observations and adaptation decisions in
[round 4](research/ROUND-04-LANDING-PAGE.md). The
[landing page plan](experience/LANDING-PAGE-PLAN.md) defines audience, draft hero,
six sections, CTA behavior, chat storyboard, evaluation explanation, visual tokens,
compatibility wording, LP-01–08 and later validation gates. No page, GIF, deployment
or product code was created. No user research or host acceptance run is claimed.
No Git remote is configured, so the public destination remains unresolved.

## I-06 — project-first UI correction, 2026-10-21

User rejected the prior palette/branding and unclear information/action hierarchy.
Removed visible decorative branding; neutralized colors and display typography;
retained top navigation; prioritized a continuation prompt for the actual saved
next action; made Guides task-based and optional; changed Files & diagnostics to
Project health with technical data collapsed. Core pages explain purpose and
where work happens. [Evidence](experience/evidence/ui-03/RESULTS.md): 35 tests,
seven browser fixtures, 24 layout checks passed. User acceptance remains pending.
The previous green visual direction is superseded, including its reuse proposal
for the landing page. Landing page remains research/planning only.

## I-07 — visualization-only viewer, 2026-10-21

User corrected the product scope: the viewer visualizes the system built in an
external agent. It does not guide work. Removed next actions, continuation prompts,
learning UI and stage tracking; added an actual source/rule/check overview map.
Main navigation has four content inspection views. Diagnostics are secondary.
[Evidence](experience/evidence/ui-04/RESULTS.md): 35 tests, seven fixtures and
16 layout checks passed. This supersedes I-06 workflow-interface assumptions.

## I-08 — visual dashboard refinement, 2026-10-21

User requested more visual structure and less repeated labeling/text. Added
category diagram, recorded-connection bars, source reference/method distributions,
compact source cards, two-column checks and progressively disclosed relationship
details. Removed repeated page eyebrows. No workflow features returned.
[Evidence](experience/evidence/ui-05/RESULTS.md): 35 Python tests and final seven
browser fixtures/16 layouts, with diagram assertions and no observed errors.
Visual/user acceptance remains pending.

## I-09 — public landing page implementation, 2026-10-21

User accepted the current viewer direction, requested landing page execution and
specified future GitHub Pages hosting. Corrected repo destination supplied by the
user is jeremydhoover-blip/fievel-content-system. Implemented the six-section page,
static chat storyboard, system illustration, evaluation chain, compatibility
qualifiers, clone/prompt copy controls and manual-copy fallback. Buildless assets
are in website/dist. Manual-only Pages workflow uploads that directory alone.

[Evidence](experience/evidence/landing-page-01/RESULTS.md): five browser widths,
keyboard skip link, copy success/denial, reduced motion, root and project-subpath
asset loading; 35 existing tests and eight adapter checks passed. A missing favicon
was fixed after the first reachable browser run. Initial isolated preview timed
out; a reachable local server was used for successful checks. No push or deployment,
visitor study, independent accessibility certification or new host acceptance run.

## I10 Landing page revision planning

2026-10-21. User reviewed the first page and requested a documented plan before
confirming implementation. Recorded strict writing preferences, replacement
copy, a concrete four-entity relationship model, a six-message animated chat
storyboard and section-specific design/interaction proposals in the
[revision plan](experience/LANDING-PAGE-REVISION-02.md). Inspected W3C diagram and
motion guidance plus MDN media-query behavior. No website implementation was
changed. User confirmation is required by this explicit request before execution.

## I11 Landing page revision implementation

2026-10-21. User confirmed the revision plan. Implemented replacement copy,
writing constraints, logical four-entity map, controlled animated conversation,
synchronized artifact, foundation tabs, host setup selector and evaluation
explanation. [Evidence](experience/evidence/landing-page-02/RESULTS.md) includes
before assets, screenshots and browser outputs. Five widths, full playback and
reduced-motion/no-JS checks passed. 35 core tests and eight adapters passed.
No push or deployment. User review and independent accessibility/visitor evidence
remain open.

## I12 Fievel focused landing page correction

2026-10-21. User rejected the booking-focused revision and explicitly instructed
execution of a Fievel-focused correction. Replaced the domain example with the
content-system ontology, onboarding greeting and product-level foundation and
evaluation content. Removed the file artifact and disclaimer.
[Evidence](experience/evidence/landing-page-03/RESULTS.md) records five-width
browser checks and the preserved previous assets. The four-entity booking plan is
superseded by this user direction. No publication occurred.

## I13 Connected map and concise sections

2026-10-21. User feedback identified that the responsive map had become a list
and requested meaningful detail with less repeated copy. Preserved the demo and
host section. Replaced the mobile list with a scrollable connected bubble graph,
added numbered expandable setup topics, simplified the content-system tabs,
created an evaluation branching flow and renamed the final setup section.
[Evidence](experience/evidence/landing-page-04/RESULTS.md) records five responsive
widths and interaction checks. No publication or backend change.

## Current work state

Updated after I13

| Work | State | Evidence / next step |
|---|---|---|
| Baseline/audit/research round 2 | Recorded; open questions explicit | Dated audit and research ledger; not independent product acceptance |
| WP-01 | Implemented and locally verified | 23-test suite, preserved pre-fix failures, ADR-001 |
| WP-02 | Definitions/protocol ready; no behavioral runs | Run FB-01/02/03 in clean contexts; no fabricated results |
| WP-03/04 | Planned | Specify review evidence/rubric and execution-coverage semantics |
| WP-05/06/07 | Planned | Adapter ownership; example entry/naming; learning objectives |
| WP-08 | Partly addressed | File/source snapshots and iterations exist; Git history, dependency locking and CI execution pending |
| WP-09 | First functional UI accepted; heuristic refinement locally verified | Intended-user tasks and independent accessibility review pending |
| WP-13 | Landing page implemented and locally verified; publication pending | LP-01–08; Pages execution, public destination content and visitor/host evidence remain unverified |
| WP-10 | First-use/return journey specified | Observed beginner/expert/resume behavior still pending |
| WP-11 | Three expanded draft lessons and routing added | Independent content review, learner outcomes and offline-routing behavior pending |
| WP-12 | Quality/consumer boundaries specified and explained locally | Evidence locators/approval model and actual consuming-agent integration pending |


## I14 Landing page labels and simplification

2026-10-21. Applied user wording/layout edits. Hero CTAs are Get started and Learn
more and navigate to page sections without starting playback. Map explanation
is always visible below dynamic detail with a thin divider. Renamed the process
heading How it works and the topics heading What is included in your system.
Merged the tabbed breakdown into that section, removed its redundant heading
and supporting sentence, transcript, separate replay button, compatibility
paragraph and footer prototype/license text. The single demo button handles
play, pause, resume and replay. Five-width browser checks passed, including
assertions that Learn more does not start playback and only one playback button
exists. Nothing published.


## I15 Landing page motion and design guide

2026-10-21. User requested animations, hover feedback and a site design guide,
with layered color and visual depth as the following pass. Added fine-pointer
control lift, directional link feedback, graph incident-edge highlighting for
hover/focus/selection, one-time section entrances and disclosure transitions.
Reduced motion cancels decorative animation. Default content remains visible.
[Design guide](../website/DESIGN-GUIDE.md) records current tokens, typography,
writing rules, interaction boundaries and the proposed next visual-depth work.
Five-width browser checks passed including graph hover/focus connection counts,
playback, no-JS and reduced-motion behavior. Results are in
[the evidence file](experience/evidence/landing-motion-01/results.json).
No new color palette or deployment was introduced.


## I16 Local surface depth draft

2026-10-21. User requested design-guide review, site updates and a workspace preview.
Reviewed website/DESIGN-GUIDE.md and implemented its proposed neutral/violet surface
hierarchy for WP-13 and LP-01–08. Consolidated foundation tokens and refined graph,
chat, evaluation and agent-selector surfaces. Previous CSS preserved in
experience/evidence/landing-depth-01/styles.css.before.txt. Content and interactions
remain intact. Browser checks passed at 1440, 1024, 768, 390 and 320px without page
overflow or script errors, including selection, copy fallback, playback, reduced
motion and no-JS reading. Inspected desktop screenshot. 35 core tests and eight
adapter checks passed. Initial sandbox Edge startup failed; isolated browser checks
succeeded outside the sandbox. Palette approval and user review remain open.
No publication performed. Next action: user reviews the local visual draft.


## I17 Visual redesign plan after palette feedback

2026-10-21. User rejected the accumulated color revisions and explicitly requested
a documented plan. Created website/VISUAL-REDESIGN-PLAN.md with proposed palette,
section treatments, gradients, elevation and verification sequence. Updated the
design guide to point to this proposal. No site assets changed in this step and
no new tests are claimed. Next action: user reviews the proposed direction.


## I18 Terracotta visual plan implementation

2026-10-21. User authorized I17. Implemented the palette, gradients and elevation
plan for WP-13 and LP-01–08. Preserved prior CSS in landing-terracotta-01 evidence.
Removed superseded surface patches and consolidated color and shadow tokens.
Desktop and mobile full-page screenshots inspected. Browser checks passed at
1440, 1024, 768, 390 and 320px with no page overflow or script errors; graph
scrolling remains local on narrow screens. Playback, keyboard selection, copy
fallback, live reduced motion and no-JS reading passed. 35 core tests and eight
adapter checks passed. Contrast pair measurements saved separately; no independent
accessibility or visitor acceptance claimed. No publication. Next action: user
reviews the local page.


## I19 Graph correction planning

2026-10-21. User screenshot and feedback reject the graph's beige treatment,
ovals and clipped scrollable layout. Documented website/GRAPH-REDESIGN-PLAN.md.
The previous five-width checks permitted local graph scrolling; they did not
establish visual acceptance. Proposed full-width desktop graph and compact
relationship presentation remove that assumption. No site assets changed or
new checks executed. Next action: review correction plan before implementation.


## I20 Product readiness and execution reporting

2026-10-21. User accepted UI direction and shifted focus to product functionality.
Readiness audit and disposable CLI probes: audits/2026-10-21/product-readiness/REVIEW.md.
Baseline 35 tests and eight adapters passed. Reproduced F-04 zero-execution success.
Added explicit CLI execution, missing-response and human-review counts. Two new
tests failed before repair; all 37 pass afterward. Reports and exit codes preserved.
No fresh agent journey or human review claimed. Next: WP-02 clean-context anchor
journeys and WP-03 evidence contract. F-02/03/05 and product acceptance remain open.


## I21 Prepared guided-authoring trials without model calls

2026-10-21. User authorized proceeding, then explicitly selected trial preparation
without model calls. Prepared FB-01/02/03 candidate explicit-read inputs under
evals/fievel-behavior/prepared-2026-10-21. Workspaces freeze guidance and code;
prompts and expected observations remain outside target workspaces. FB-03 starts
from a blank package with the specified draft rule, saved no-tool decision and
unrelated sentinel. All initial file hashes and exact user turns are preserved.
Read-only verification passed for all three bundles. Initial isolated validation
correctly reported missing jsonschema; retained that evidence. Revalidation using
existing root dependencies passed default validation/status and rejected uncovered
rules in strict mode. No dependency installation, model call, agent journey or
human judgment executed. All cases remain not_run and WP-02/V-05 remain open.
Next action: run trials in fresh sessions when authorized; WP-03 evidence/rubric
contract design can proceed independently. Current UI remains accepted.


## I22 Self-contained human review evidence and completion validation

2026-10-21. User authorized human-review evidence and validation work. ADR-003
records contract and migration choices. Added opt-in evidence review preparation,
review configurations with rubrics/excerpts/origins, frozen context/hashes and
validate-review with optional current-package and completion gates. Legacy report
formats remain unchanged. Eleven new tests bring the total to 48 passing; eight
adapter checks pass. Example/template validation passes. Generated six pending
fictional judgments, without claiming human decisions. Results and test logs are
in audits/2026-10-21/review-evidence. WP-03 software contract implemented; two-person
rubric calibration remains open. Next action: independent review using saved context
and provisional refund examples; WP-02 model execution remains unauthorized.


## I23 Generated adapter ownership

2026-10-21. User authorized offline adapter maintenance. ADR-004 documents the
manifest and no-delete lifecycle. Added owned-path/hash recording, first-migration
adoption, stale-copy and local-edit detection, and confined output paths. Eight
new isolated tests pass; full suite has 56 passing tests. Production sync adopted
eight matching outputs; --check passes. Unrelated skills are preserved and conflicts
stop sync before writes. Pre-manifest orphans cannot be reliably identified and
remain a documented migration limit. No model or native host execution. Evidence:
audits/2026-10-21/adapter-ownership/RESULTS.md. Next: source provenance validation.


## I24 Offline source provenance validation

2026-10-21. User authorized source provenance checks. ADR-005 records scope and
status semantics. Added sources-audit with explicit as-of date, optional age window
and explicit evidence/conflict input. Missing metadata and evidence warn; invalid
dates and broken evidence references error. No source ingestion, authority
authentication or semantic conflict detection claimed. Nine new tests bring total
to 65 passing; eight adapters match. Example/template package validation passes.
Actual metadata-only and supplied-evidence CLI reports are saved under
audits/2026-10-21/source-provenance. Existing package schema unchanged.
No model calls or human review executed. Next: malformed-input hardening and
consumer contract design; source meaning/authority and human rubric calibration
remain open.


## I25 Malformed input hardening

2026-10-21. User authorized offline input hardening. Preserved failing probes
and repaired strict JSON loading, path-specific parse errors, explicit 128-level
nesting cap, serialization before output creation and explicit-null provenance
rejection. Viewer and adapter manifest use shared strict parsing. Seven new tests
bring full suite to 72 passing; eight adapter checks pass. No model calls or source
ingestion. Evidence: audits/2026-10-21/input-hardening/RESULTS.md. Existing valid
schemas unchanged; ambiguous/nonstandard JSON is now intentionally rejected.
Next offline work: consumer export contract design.


## I26 Consumer review export contract

2026-10-21. User authorized consumer export work. ADR-006 defines named consumer,
declared-approved default selection, explicit draft option and review-only boundary.
Implemented export-consumer preserving exact rules/status/provenance and separating
unreviewed context from instructions. No automatic tool grants or installation.
Six new tests bring suite to 78 passing; eight adapter checks pass. Actual CLI
export of five fictional draft rules saved under consumer-export audit evidence.
No model calls or source fetching. SYS-02 integration behavior remains untested.
Next offline work: clean-setup verification with available local dependencies.


## I27 Isolated offline setup verification

2026-10-21. User authorized offline setup checks. Added a reproducible runner
creating a new workspace and venv, with no downloads or model calls. Sandbox
temporary-folder permissions blocked bootstrap; local temp resolved that. Offline
pip could not find jsonschema, so clean dependency installation stays unverified.
Copied existing local dependencies as an explicitly separate recovery path. Full
CLI workflow passed. Initial clean-copy suite exposed 14 test setup errors from
missing .scratch; fixed test setup and reran from another fresh copy. All 78 tests
passed; eight adapters match. Evidence: offline-setup-final RESULTS.md and earlier
retained failure records. Verified Windows/Python 3.12.10 runtime recovery only.
Next gates: authorized wheelhouse/install evidence, independent human calibration,
and fresh agent/consumer behavior when authorized.


## I28 Human calibration preparation

2026-10-21. Continuing authorized offline work, prepared two independent reviewer
folders with three authored refund cases each. Preserved complete evidence, neutral
case IDs, blank human metadata and twelve pending judgment slots. Organizer-only
expectations and comparison worksheet remain separate. Validated all six evidence
records; no human judgments, agreement counts or outreach performed. Source
project and current UI unchanged. See evals/human-review-calibration/round-01/README.md.
Next action requires two actual reviewers; model calls and downloads remain off.


## I29 Readable offline human review pages

2026-10-21. User authorized local review forms. Added review-page, self-contained
HTML evidence rendering, editable metadata/judgments and JSON download. Inputs
remain unchanged, missing responses are disabled, no-JS reading works and Python
validation remains authoritative. Four new tests bring suite to 82 passing; eight
adapters match. Browser checks cover synthetic download/CLI round trip, invalid
quotes, keyboard order, narrow layout and no external requests. Six calibration
pages generated with all human judgments still pending. Evidence: review-page
RESULTS.md. No model calls or human completion claimed.


## I30 Repository readiness and product value plan

2026-10-21. User requested repository reliability and demonstrated product value
before plugin development. Added REPOSITORY-READINESS-PLAN.md with staged gates,
end-to-end acceptance journey, comparative study, responsibilities and RP-01–07
actions. Added research/ROUND-05-PRODUCT-VALUE.md with a dated primary-source
market scan. Existing tools overlap; differentiation remains a hypothesis.
Reviewed I29 evidence and the unrun behavioral-trial preparation. No new tests,
model calls, participant sessions, publication or plugin implementation performed.
Next action: RP-01 claim-to-evidence ledger and prioritized gap audit.


## I31 Local Codex plugin pilot

2026-10-21. User authorized a local Codex plugin pilot and live model trials;
CODEX-PLUGIN-PILOT.md supersedes the earlier plugin deferral. Added plugin-src/
manifest and entry skill, build_plugin.py hashed self-contained bundle in
plugins/fievel, local fievel-local marketplace and run_plugin_pilot.py. Suite has
83 passing tests; eight adapters match. Codex 0.162.0-alpha.17.2 installed
fievel@fievel-local 0.1.0. Recorded codex exec trials (evidence kept out of Git
in .scratch/plugin-pilot): approved-execution found the plugin but its configured
Python executable was missing, so nothing was created; codex-runtime, with a
prepared venv on PATH, initialized Wayfarer, passed coverage validation, generated
a viewer and saved the skip-lessons decision and next action, reporting all stages
draft; documents-workspace initialized a system, then failed on a ChatGPT usage
limit before validation or a final report. A resume trial was prepared against
the codex-runtime workspace but has no execution record. Every run warned that
icon_small/icon_large paths with '..' were ignored; the bundle defines no such
fields, so the cause is unconfirmed. PLUGIN-READINESS.md records the acceptance
ledger. Not proven: missing-Python recovery, resume, real sources, Jeremy's
hands-on trial, desktop UI refresh. No publication or outreach. Next action:
rerun the resume and Documents trials after the usage limit resets.


## I32 Claude Code plugin bundle

2026-10-21. User requested a Claude Code plugin from the same sources. Checked
the current Claude Code manifest, marketplace and skill documentation. Added
build_plugin.py --target claude (Codex remains default): derived
.claude-plugin/plugin.json, identical skill and runtime bytes, logo as icon.
Built plugins/fievel-claude and a root .claude-plugin/marketplace.json
(fievel-content-system). Four new tests cover target layouts, a relocated Claude
bundle running init and strict validation, committed-bundle drift for both hosts
and catalog paths; a deliberate bundle edit made the drift test fail. Full suite
has 87 passing tests; eight adapters match. The existing Codex bundle still
matches a fresh build. No claude CLI was available, so claude plugin validate,
installation and any Claude session behavior are unrun. Evidence: the tests and
CLAUDE-PLUGIN-PILOT.md. Next action: validate and install in Claude Code, then
run the shared trial tasks.


## I33 Plugin release cleanup

2026-10-21. User requested all six skills in both plugins and no internal status
wording in public text. Replaced the single `fievel` router skill with the six
canonical skills, each generated with a shared plugin-src/skill-preamble.md
(runtime path, setup and handoff rules) after its title; getting-started is the
Codex onboarding skill. Fixed the "Ai" title typo in the canonical skill and
synced adapters. Rewrote the plugin long description, both catalog descriptions
and the README introduction without pilot/validation status, and added an
install-as-plugin section. Internal evidence docs keep their status records.
Rebuilt both bundles; two new tests cover the six-skill set, preamble placement,
onboarding path and public manifest wording. The installed fievel@fievel-local
cache still holds the earlier one-skill bundle at the same 0.1.0 version.
Not run: any host session with the new skills, claude plugin validate, and the
README's Codex marketplace instruction against a published repository.


## I34 Pre-push readiness check

2026-10-21. User asked to confirm repository, local viewer, landing page and both
plugins before the first push. Fresh clone: the nested my-content-system/ ignore
rule had excluded the FB-03 prepared package, so verify.py failed; anchored the
rule to the root folder, tracked the fixture and added verify.py to CI. Fixed two
Windows-1252 bytes in ITERATIONS.md. All doc and landing links resolve. From the
clone: 89 tests, adapter sync, evidence verification and reproducible bundles pass.
Viewer and review-page browser suites pass; README exercise and viewer render
without errors at 1440 and 390. Landing: logo reduced from 1.09 MB to 106 KB,
Fievel favicon and touch icon, share tags, theme colour, no-wrap code; browser
suite passes with no external requests. Claude Code 2.1.304: plugin and catalog
pass validate --strict; isolated install lists six skills. Codex 0.162.0-alpha.17.2:
renamed catalog to fievel-content-system; isolated install and prompt render list
six fievel:* skills with no icon warnings. README now has exact install commands.
Not run: a live model session in either host, a GitHub-sourced install, the CI
matrix and the Pages deployment.


## I35 Directory submission preparation

2026-10-21. User asked to prepare both plugins for directory submission and will
submit personally. Version raised to 0.2.0. Added plugin-src/README.md as the
bundle README, homepage/repository, Codex websiteURL/supportURL/privacyPolicyURL
and release notes, and Claude documentationUrl/supportUrl/privacyPolicyUrl.
Added website/dist/privacy.html, linked from the landing footer. Rebuilt both
bundles; a new test covers listing URLs, README length and Anthropic's file size
and count limits. 90 tests pass; adapters match; landing suite passes. Claude Code
validate --strict passes; the Codex ZIP (release/, ignored) matches the bundle and
installs as 0.2.0 with six skills in an isolated home. PLUGIN-SUBMISSION.md holds
listing values, steps and draft data-handling answers. Not run: either directory's
scan or review, a live model session, and the privacy page on the deployed site.


## I36 Claude directory name hold

2026-10-21. The Anthropic directory validation passed with warnings and held the
name for review: NAME_CONFUSABLE, "fievel" against the connector "level". The
portal allows changing name, displayName or author.name. Set displayName
"Fievel Content System" in the derived Claude manifest and catalog entry, keeping
name `fievel` so install commands and skill namespaces are unchanged. Unknown-key
warnings for documentationUrl, privacyPolicyUrl, supportUrl and icon are expected
listing fields. 90 tests pass; validate --strict passes; an isolated install shows
"Fievel Content System (fievel) 0.2.0". Not run: the portal's revalidation.


## I37 Live Claude Code plugin trial

2026-10-21. User authorized live Claude Code sessions after questioning product
quality. Ran the published 0.2.0 plugin headless in a clean folder outside the
repository with a fictional home-energy assistant and style guide: six resumed
turns plus a fresh-session resume. Fievel set up dependencies locally, captured
the brief, imported sources with provenance, defined 18 rules and 10 situations,
caught all three seeded response violations plus an unseeded data mismatch,
handled a source change with history, and resumed from files alone. Independent
re-run reproduced the check report; all human items stayed pending. Findings
LT-01 (progress in fingerprint makes reports stale), LT-02 (source-discovery not
routed), LT-03 (denied PowerShell/compound commands) and LT-04 (cost growth).
Evidence: audits/2026-10-21/live-claude-trial/RESULTS.md. Not run: Codex, an
interactive user, content-audit, real sources.


## I38 Live-trial fixes: content fingerprint, source routing, simple commands

2026-10-21. User asked to fix LT-01, LT-02 and LT-03 from I37. ADR-007: reports,
review sheets, viewer snapshots, consumer exports and source audits now record
system_sha256 over content files only, with system_scope "content"; progress.json
is excluded. Review evidence moves to 1.1. Reports without a scope and evidence
1.0 keep the seven-file meaning through matches_system, so stored evidence is not
rewritten and still reproduces or goes stale as before. Five new tests cover
progress edits, content and governance edits, viewer reproduction, legacy files
and unknown scopes. LT-02: content-system-builder now hands supplied documents to
source-discovery first, whose description names that trigger. LT-03: the plugin
preamble asks for one simple Python command per step and host file tools for
reading. Version 0.2.1; bundles and Codex ZIP rebuilt. 95 tests, adapter sync,
evidence verification, viewer and review browser suites and Claude validate
--strict pass. Not run: a live session confirming LT-02 and LT-03 behavior.


## I39 MCP servers for Claude Code and the Codex directory

2026-10-22. OpenAI's portal rejected the skills-only draft ("We are not
accepting more skills-only submissions at this time"); the user chose local and
remote MCP servers and Google Cloud Run hosting. ADR-008: a dependency-free MCP
layer with shared lesson, template and format tools; a stdio local server wrapping
the CLI inside FIEVEL_WORKSPACE, shipped in the Claude bundle via .mcp.json; and a
stateless HTTP remote server for the Codex bundle (mcp.json added once its URL is
set), with a 2 MiB cap, no batching, no content logging and a domain-challenge
route. Added evaluate_data, Dockerfile, .gcloudignore/.dockerignore, MCP-SERVER.md
deploy guide, privacy and terms sections for the hosted server, skill preamble
guidance, Codex test cases and version 0.3.0. 100 tests pass; Claude validate
--strict passes and an isolated install reports the local server Connected; the
remote server runs from the container's file set. Not run: Cloud Run deployment,
domain verification, OpenAI tool scan, a live session using the tools.
