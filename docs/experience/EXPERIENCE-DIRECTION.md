# Experience direction: guided authoring, a visible system, and local knowledge

Status: design proposal and validation plan, 2026-10-21. Source: the user's latest
direction, extending the original brief. The experience is the main product:
getting started, making useful decisions, seeing what was created, checking it,
and returning later should feel like one guided process.

## Scope change

The original brief deferred a graphical product. The user now explicitly expects
a pleasant UI for viewing the content system and its relationships. Add a small
local companion view to the core experience. This is a requirement change, not a
reason to build a hosted SaaS or move ownership out of repository files.
The original brief is preserved; this document records the amendment.

## Three connected workstreams

| Workstream | User outcome | What currently exists | What we need to validate |
|---|---|---|---|
| Guided experience | “I know where to begin, what we just made and what to do next.” | Paths, stage guide, progress file and skill instructions | First-use journey, focused questions, progressive explanations, brief expert path and return session |
| Content-system quality | “My standards are represented faithfully and can guide an AI experience.” | Structured files, example rules, links and checks | Evidence-to-rule fidelity, ambiguity/conflicts, instruction composition, actual consumer behavior and review criteria |
| Bundled knowledge | “Fievel can explain and guide ordinary work from material already here.” | Four introductory modules | Useful local lesson depth, task-based routing, misconceptions, source currency and separation from company policy |

The UI supports all three: it makes relationships visible, opens the relevant
explanation, and helps the designer choose the next conversation. A beautiful
viewer cannot compensate for weak rules or missing guidance.

## First-use journey to design and test

| Moment | Designer sees/does | Fievel's responsibility | Evidence saved |
|---|---|---|---|
| Get the repository | One plain-language start instruction; prerequisites and access costs clear | Detect what is actually available, explain the local workflow; do not require a connector or paid API key | Only setup limitations relevant to this project |
| First exchange | A brief introduction and three routes; use intent already supplied | Identify new/guidelines/AI-experience path; do not repeat questions already answered | Path and explanation preference |
| First useful decision | Describe one task, or choose a specific existing standard | Explain one relevant concept, draft a small artifact, show it immediately | Product context, draft rule, unknowns and next step |
| First visible system | Overview even when mostly empty; one concrete relationship when available | Show what exists, what is missing, and why a connection matters | Viewer derived from current package, with snapshot/freshness indication |
| Bring team material | Select an authorized local guideline and inspect a proposed mapping | Preserve wording, authority and unresolved interpretation; avoid silently replacing company standards | Source inventory, evidence locator, rule status and decision |
| Define/check quality | A realistic situation and an appropriate literal/human check | Explain why the method fits, show defined versus run versus reviewed | Definition, actual evidence if present, review questions |
| Leave/return | Last decision and next action visible; no repeated onboarding | Read saved state, identify relevant changes and continue | Updated progress and governance decisions |

The first useful artifact should appear after a small number of purposeful
decisions. We have not established a fixed number of turns or measured time to
value. Test that people can explain their first artifact, not just receive files.

## Recommended UI hypothesis

Default to a guided **Overview**, with a focused **Connections** view. Both use
the same files and selected item. The overview answers purpose, next action,
decisions still open and actual artifact status. Connections explain a selected
source → rule → check relationship, with inspectable details and an equivalent
linear text view. Keep a full graph optional until it helps with a demonstrated
scale/navigation problem. See [VIEWER-DESIGN.md](VIEWER-DESIGN.md).

First local viewer implementation should be read-only. The agent remains the
authoring partner and files remain authoritative. “Read-only” is an initial
engineering choice, not a permanent restriction on the product. Add editing only
with clear save/conflict/approval behavior and tests for preserving user work.

## Content quality is more than schema validity

Distinguish five layers: Fievel's core teaching instructions; reusable workflow
skills; the designer's product/rules/behavior; their organization’s source material;
and the instructions supplied to a consuming AI experience. The current JSON files
describe a system but do not automatically install or enforce it in another agent.

For each brought-in standard, inspect: exact source location, who approves it,
scope/context, what is explicit versus interpreted, and what check could establish
compliance. A source ID alone does not establish that a rule is supported by the
source. Unsupported interpretation stays draft. Conflicts need a decision, not
confident synthesis. See ../../knowledge/content-design/using-existing-guidelines.md.

Plan a reviewed instruction-composition/export experiment: assemble a small
consumer instruction set from selected rules and context, include boundaries and
source use, show it to the owner, then test with actual responses. Do not claim
“AI-ready” means the model will obey or that a skill grants tools/permissions.

## Local knowledge policy

Ordinary explanations and fictional practice should work using bundled lessons,
templates and examples. Organizational material stays a separate source inventory.
External browsing is an intentional supplement for current tool behavior, new
topics and source verification; it should not be a requirement for explaining a
content principle already covered locally. An offline lesson can be useful while
still having a review date and known gaps. See [KNOWLEDGE-ARCHITECTURE.md](KNOWLEDGE-ARCHITECTURE.md).

## Design validation before a viewer is called useful

Ask a beginner to find the next step, explain where a rule came from and tell
whether a check has run. Ask an experienced practitioner to trace the impact of
changing a term/policy and find the original rule/source. Compare overview-led and
connection-led designs using the same package. Observe errors and explanation
quality, not aesthetic preference alone. Include keyboard use and linear reading.

The conversation prototypes are design alternatives with fictional data and do not
establish usability. Following the user's instruction to proceed, the overview-led
real-file snapshot is now implemented under ADR-002. It is read-only, surfaces
diagnostics and checks explicitly selected reports. The next gate is actual designer
tasks and independent accessibility evaluation; local browser tests alone do not
establish those outcomes. There is no live file watcher or editing interface.


## Viewer scope correction — user direction, 2026-10-21

The companion UI is a visualization dashboard of the content system created in
an external agent. It shows product context, rules, sources and quality-check
connections/results. Guidance, lessons, next actions and progress tracking belong
in the agent experience, not this viewer. This supersedes earlier proposals to
put those workflow features in the dashboard. See
[I-07](../ITERATIONS.md).
