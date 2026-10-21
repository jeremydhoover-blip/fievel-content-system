# Live Claude Code plugin trial 01

2026-10-21. First live end-to-end use of the published Fievel plugin (0.2.0) in
Claude Code 2.1.304, authorized by Jeremy. Fictional product and sources only;
session transcripts and workspace stay outside Git.

## Setup

- Workspace: a new folder outside the repository (`Fievel Plugin Trials/cc-01`)
  holding only `keep.txt` (sentinel) and a fictional `sources/lumen-style-guide.md`
  for "Lumen", a home-energy app support assistant.
- Plugin: a copy of `plugins/fievel-claude` loaded with `--plugin-dir`; no repository
  instructions available. System Python 3.12 without jsonschema.
- Headless `claude -p`, one scripted user turn per call, resumed in one session;
  turn 7 was a new session. Permissions: file edits plus Python and simple listing
  commands; web tools disabled. Model usage equivalent to about 9.34 USD (Max plan).

## Turns and outcomes

| Turn | Request | Outcome |
| --- | --- | --- |
| 1 | Start as an experienced designer; set up dependencies | Correct introduction, skipped lessons, created `.fievel-venv` with jsonschema locally, initialized the project, noticed the style guide but asked before reading it |
| 2 | Product brief | Recorded only what was given; objectives left as an open question; flagged that "report an outage" had no defined capability |
| 3 | Outage answer; import the approved guide | Recorded the source with owner/date; mapped rules with line-level provenance in a note; kept its own wording as draft; flagged the guide's "(fictional)" owner label, a term/jargon tension and an uncovered safety case |
| 4 | Bill-cause limits; behavior and checks | 18 rules and 10 situations (ordinary, unknown, suggested cause, unclear, action requests, conflicting sources); strict coverage passed; stated no checks had run |
| 5 | Approve drafts; check four saved responses | Caught all three seeded violations (savings percentage, false "Done!" payment change, false outage report plus "click here" and missing status link); also found that the "good" response's dates did not match the situation it defined; AI reading labeled as suggestions; human questions pending |
| 6 | Source changed: "energy use", never "consumption" | Retired the old rule with history, added the new approved rule, updated situations and checks, logged governance changes, returned "usage" synonym to draft for a decision, re-ran checks, deleted superseded reports |
| 7 | New session: resume | Rebuilt decisions, ten open questions, run-01 results and next step from saved files; no re-onboarding, no repeated questions |

## Independent verification

- `validate --require-coverage` passes on the final package.
- Re-running `check` with the same responses reproduces the saved report exactly:
  same system fingerprint, 8 pass, 5 fail, 29 not run.
- Review sheet: 27 human items, all `pending`; no fabricated judgments.
- Rule statuses match user decisions: 17 approved, `content-term-usage` draft.
- Remaining "consumption" occurrences are the avoid list, the rule text and the
  checks for its absence. `keep.txt` unchanged. Generated overview renders with
  no errors and no network requests.
- Skills invoked: getting-started (both sessions), content-system-builder,
  ai-behavior-designer, evaluation-designer.

## Findings

| ID | Severity | Finding | Recommendation |
| --- | --- | --- | --- |
| LT-01 | Medium | The system fingerprint includes `progress.json`. Fievel saves progress after each step, as instructed, which makes every report and overview stale immediately; turn 5 produced three report versions and four overviews before cleanup. | Exclude session bookkeeping from the fingerprint, with a recorded migration for existing reports (ADR) |
| LT-02 | Low | Importing the style guide was handled by content-system-builder; source-discovery was not invoked. Provenance was still recorded well. | Review routing text so source inventory requests reach source-discovery |
| LT-03 | Low | On Windows it tried PowerShell and compound shell commands; 9 were denied under the restricted permissions. Interactive users would see extra permission prompts. | Preamble guidance: one simple Python command per step |
| LT-04 | Info | Later turns cost far more (up to 3.2 USD equivalent) as context grew. | Consider fewer intermediate files and shorter summaries |

Not covered: content-audit and source-discovery skills, Codex, an interactive
(non-scripted) user, real organizational sources, and learner understanding.
Scripted turns by the developer are not independent usability evidence.
