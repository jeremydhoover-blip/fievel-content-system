# Compatibility evidence

Reviewed 2026-10-21. Distinguish file-format checks from host runtime evidence.

| Environment | Evidence | Remaining check |
|---|---|---|
| Current Codex desktop engineering session | Repository files authored/read; CLI and Python tests run through shell tools | Start a fresh project session, verify native skills discovered, complete and resume a guided conversation |
| Current session after skill catalog refresh | Six Fievel skill names/descriptions/paths appear in the available-skills catalog | Invocation, output quality and fresh-session reproducibility still need observed runs |
| Codex CLI / IDE | Official documentation checked; AGENTS.md and .agents skill paths supplied | Independent CLI/IDE activation and behavior test |
| Claude Code | Canonical skills copied to .claude/skills; sync drift checked | Trust workspace, invoke /getting-started, finish/resume exercise |
| VS Code agent/Copilot | Copilot instruction adapter and .agents skills supplied per documentation | Check extension/version settings, skill selection and saved-progress behavior |
| Python CLI | Windows/Python 3.12 exercised locally | CI matrix for Linux and Python 3.10 is configured, not yet executed remotely |

## Repeatable host acceptance exercise

1. Record host/version and start a fresh session in the repository root.
2. Invoke getting-started using the host's skill interface. If missing, record the
   discovery failure and use “Read AGENTS.md and start Fievel.”
3. Choose beginner/Wayfarer, explain one product task and inspect generated files.
4. Verify the agent distinguishes draft guidance from approved policy and defined
   checks from executed results. Run both saved-response fixtures.
5. Review the invented refund claim in the literal-pass fixture; ensure human
   questions do not get reported as automatic passes.
6. End the session; open another supported host and resume from progress.json.
7. Try an experienced path and confirm lessons can be skipped.
8. Record actual transcript excerpts, failures and changed files. Do not change this
   table to “verified” based on a generated adapter or static test alone.
