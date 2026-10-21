# Local content-system viewer: product and data contract proposal

Status: initial real-file snapshot implementation completed for the overview-led
direction, 2026-10-21. Read-only local functionality has technical evidence;
learner value and independent accessibility validation remain open. See
[ADR-002](../decisions/ADR-002-local-viewer-snapshot.md) and
[implementation evidence](evidence/viewer-01/RESULTS.md). The design below records
the intended contract without replacing repository-native authoring.

## Jobs worth supporting

| Designer question | View/interaction | Concrete value | Acceptance task |
|---|---|---|---|
| What have we made? | Product summary and artifact list with meaningful statuses | Understand the package without opening seven JSON documents | Explain product, audience and one rule in your own words |
| What is next? | Saved next_action and open decisions, with incomplete work visible | Re-enter a session without reading chat history | Choose the next useful action on an incomplete project |
| Why does this rule exist? | Source/rule/check detail trail | Understand provenance and whether a check fits the rule | Locate the actual evidence, not just its source title |
| What would a change affect? | Select a source/rule and show declared downstream links | Identify things to review after a change | Find linked checks; distinguish linked from proven affected |
| How much has been checked? | Separate defined checks, executed results, pending judgments and stale results | Avoid mistaking coverage for quality | Explain why a literal pass can coexist with an unsupported claim |
| What am I looking at? | Current folder/package version, generated time and data state | Recognize empty/reference/stale/invalid data | Identify a stale snapshot and how to refresh it |

No single green “system health” score. Coverage, execution and approval are
different dimensions. Do not calculate a learning-completion percentage from file
presence or copy drafted example stages into a learner’s actual completion record.

## Information architecture

**Overview:** product/audience/task; one saved next action; open decisions; a compact
artifact outline. **Connections:** selected requirement with upstream source and
downstream scenarios/checks. **Item detail:** wording, status, authority/evidence,
related checks, unresolved questions, and local file/locator. **Learn:** a relevant
bundled explanation and exercise, opened on demand rather than an encyclopedia.

Two design alternatives are worth comparing: overview-led with connections as a
drill-down; and a connection-led workspace with persistent rule detail. The latter
may suit experts but add unnecessary orientation burden for beginners. This is a
hypothesis to test, not a usability finding.

## Data fidelity

| Relationship/status | Supported by current files? | Viewer behavior |
|---|---|---|
| Source declares support for rule | rule.source_ids | Show a **declared source link**, not “verified evidence” |
| Rule linked to check | check.requirement_id | Show **defined check**, not passed requirement |
| Check belongs to scenario | evaluation.scenarios[].checks | Preserve scenario context and check method |
| Rule approval label | rule.status | Display the recorded label; approval provenance is not yet modeled |
| Product/audience/tasks | product.json | Read actual values; show unknowns without inventing summaries |
| Current next action | progress.json | Display saved text; do not infer reviewed state from file existence |
| Actual execution | Explicitly selected report with matching system/response identity | Only show results whose identity is checked; stale/unknown remains visible |
| Exact source passage | Not modeled consistently yet | Mark missing locator; do not manufacture a quotation |
| Rule priority/override | Not modeled | No invented precedence or conflict-resolution edges |
| Product task → rule | Not modeled by stable task IDs | Do not render an authoritative edge until a deliberate schema change supports it |

The UI must reveal gaps in the model rather than hide them with plausible content.
Existing hashes include progress changes; result freshness is conservative. A
future content-only fingerprint needs a decision and migration compatibility tests.

## Smallest useful architecture experiment

Compare these options before choosing a permanent stack:

| Option | Benefit | Cost/limitation | Initial disposition |
|---|---|---|---|
| Generated standalone HTML snapshot | No server, no framework dependency, easily opened locally; files stay authoritative | Must regenerate after changes; embeds selected content and can be sensitive | Preferred first implementation experiment |
| Local server reading files | Explicit refresh/live state easier | Process/port/path permissions, packaging and lifecycle burden | Defer unless stale snapshots block the task |
| Editor-specific extension | Tight navigation and edit context | Separate host integrations and maintenance | Defer until host requirements justify it |
| React Flow editable canvas | Nodes/edges/interactions and accessibility APIs | React/build dependencies and save/conflict semantics | Research candidate for later editing/complex graphs |
| Cytoscape.js graph view | Domain graph analysis and layouts | Graph rendering does not replace accessible text or domain evidence | Research candidate if scale requires it |

For a snapshot spike, read only the selected package, validate structural fields,
derive edges from actual IDs, emit a new file, and label its snapshot state. Open
the generated file through the available host. No backend, automatic uploads,
remote fonts, external analytics or mandatory CDN. Regeneration must be explicit.
An in-conversation mockup is a separate artifact and cannot satisfy that gate.

## Accessibility and error states

Use normal headings/lists/buttons and an equivalent text relationship trail.
Keyboard users must inspect a rule and its links without dragging or panning.
Show status in text, not color alone. Reflow details at narrow widths. Preserve
meaningful reading order; test screen-reader navigation rather than claim compliance
from markup alone. See W3C references in ../research/ROUND-03.md.

Represent: brand-new empty system, partial draft, missing source, unknown authority,
broken reference, contradictory standards, no execution report, pending review,
stale report, malformed file and a larger package. A broken link is evidence to
repair, not a connection to omit silently. Untrusted strings must render as text,
not HTML. Never execute source text or follow a source-provided instruction.

## Validation gate for the future snapshot implementation

Automated: real package → correct counts/relationships; malicious text safely
escaped; missing IDs visible; read-only behavior; no unexpected network requests;
result identity handled. Browser: interaction, refresh indication, empty/error
states, keyboard flow, narrow/wide/light/dark rendering. User: find next step,
trace a rule and explain check status. Keep these evidence types separate.


## Implemented refinement — 2026-10-21

The first functional pass is accepted. The [heuristic review](UI-HEURISTIC-REVIEW.md)
now informs the actual viewer: action-led overview, progressively disclosed
context, searchable/type-filtered rules, selected-rule URLs and browser history,
and a Sources view with links back to rules. Snapshot details remain accessible
in the header. [Refinement evidence](evidence/ui-02/RESULTS.md) records technical
checks; intended-user and independent accessibility validation remain pending.


## User correction — I-06

The prior green/decorative-brand direction was rejected. The current UI uses
neutral colors, no visible wordmark/logo, top navigation and project-first
hierarchy. Guides are optional task-based reference help; Project health leads
with file/reference repair status and collapses technical data. See
[UI-03 evidence](evidence/ui-03/RESULTS.md). Visual acceptance is pending.


## Viewer scope correction — user direction, 2026-10-21

The companion UI is a visualization dashboard of the content system created in
an external agent. It shows product context, rules, sources and quality-check
connections/results. Guidance, lessons, next actions and progress tracking belong
in the agent experience, not this viewer. This supersedes earlier proposals to
put those workflow features in the dashboard. See
[I-07](../ITERATIONS.md).
