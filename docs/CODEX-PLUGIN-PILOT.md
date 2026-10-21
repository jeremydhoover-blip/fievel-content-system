# Codex plugin pilot

2026-10-21. Local pilot, not a public release. Jeremy authorized model calls and
will perform the first hands-on trial himself. Broader value comparison follows
the pilot rather than blocking plugin construction.

## Active sequence

1. Focused repository checks and fixes that affect the pilot.
2. Build and install the local Codex plugin.
3. Observe fresh-session plugin behavior outside the development repository.
4. Jeremy tries a real content-system workflow; record friction and failures.
5. Fix and retest, then evaluate broader usability and comparative value.

This supersedes the original plugin deferral in REPOSITORY-READINESS-PLAN.md.
Public distribution and other hosts remain later work.

## Package design

`plugin-src/` contains the authored manifest and one Fievel entry skill. That skill
routes to the six existing canonical workflows. `scripts/build_plugin.py` builds a
new self-contained directory from an explicit set of runtime sources, with hashes.
The bundle includes no user content system, dependencies, credentials, evaluation
transcripts, or development checkout. Its Python tools execute against project paths
in the user's workspace; the installed cache is not a place to save projects.

The pilot uses the portable root plugin.json format and a local marketplace, as
documented in [OpenAI's packaging guide](https://developers.openai.com/plugins/build/plugins).
No MCP server, hosted backend, global Python installation, or public submission is
required for this pilot. Python 3.10+ and the pinned jsonschema requirement must be
available separately. Current execution evidence is Windows/Python 3.12 only.

## First human trial

Open a fresh Codex chat in a separate folder for your content-system work. Refresh
or restart Codex if the newly installed Fievel plugin does not appear. Select
Fievel from installed plugins and send:

> Start Fievel. I'm an experienced content designer building an AI experience.
> Help me build a content system in this workspace, and skip beginner lessons.

Alternatively choose the fictional Wayfarer practice when prompted. Your real
project should stay outside the installed plugin and the development repository.
If Python/dependencies are missing, allow Fievel to explain and prepare a local
environment; do not treat installation as already completed in that new folder.

Try these tasks in order:

1. Start with one product task and a few content rules.
2. Bring a small authorized source and check that its meaning and authority survive.
3. Define behavior and quality checks, then inspect the generated snapshot.
4. Supply actual saved responses; distinguish literal results from pending human review.
5. Change one source rule and see what needs updating.
6. Resume in a new chat with the project path and confirm decisions are retained.

Record the request, actual outcome, confusing step or failure, expected behavior,
affected file, and severity. Keep private source text and session logs out of Git.
Your trial provides first-person usability evidence, not independent market validation.

## Development and refresh

Build to a new directory: `python scripts/build_plugin.py --out plugins/fievel-next`.
The default target is Codex; `--target claude` builds the
[Claude Code bundle](CLAUDE-PLUGIN-PILOT.md) from the same sources.
Never hand-edit the installed cache or generated runtime. Change canonical inputs,
run the relevant tests and `python scripts/fievel.py sync --check`, then build a
new candidate, update the local catalog to that candidate, and reinstall/refresh.
Retain the old manifest with its evidence so trial results refer to exact content.

The local catalog is `.agents/plugins/marketplace.json`, named `fievel-local`.
Installed identity: `fievel@fievel-local`. The CLI in this environment supports
`codex plugin add fievel@fievel-local --json`; verify its returned installed path.
Uninstall through Codex's plugin management when desired. Project files remain
separate and are not part of the plugin cache.

## Remaining acceptance work

Installed skill discovery alone does not prove setup, source ingestion, resume,
consumer adherence, usability, or reliable model behavior. Record actual trial
outcomes in the pilot evidence report. The prepared FB-01–03 trials retain their
original unrun status unless those exact frozen protocols are executed.
