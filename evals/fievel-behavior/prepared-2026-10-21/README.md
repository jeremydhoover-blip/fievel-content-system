# Prepared Fievel behavioral trials

Prepared 2026-10-21. All three behavioral cases are NOT RUN.
User explicitly chose preparation without model calls. No agent process, model
request, participant session or human grading was started.

## Contents

| Case | Prepared input | Required observation |
|---|---|---|
| FB-01 | Fresh workspace, no user package, three exact user turns | Create library context and draft standards without inventing renewal policy |
| FB-02 | Fresh workspace with fictional guideline source, one exact user turn | Preserve all three sourced rules and propose appropriate unexecuted checks |
| FB-03 | Partial library package, saved decisions and unchanged sentinel, two exact turns | Resume without onboarding, preserve no-tool boundary and unresolved policy |

Each workspace contains frozen candidate instructions, scripts, schema, templates,
knowledge, examples and viewer assets. It contains no credentials or private source
material. The before-manifest.json hashes all initial workspace files. Prompts,
case definitions and assessment criteria live outside the workspace so the target
agent need not see the expected answers. Do not open case.json or ASSESSMENT.md in
the target agent session.

## Execution procedure when separately authorized

1. Verify initial hashes with verify.py. Copy the selected workspace to a new
   clean location before a trial. Preserve this original bundle as baseline.
2. Set up Python dependencies using the documented requirements installation.
   Preparation reused the main project's .deps for offline validation only; it
   did not test installing dependencies on a clean machine.
3. Start a genuinely fresh agent context in the copied workspace. Use a separate
   session for each case; do not carry this development chat into it. Prevent
   unrelated parent instructions, personal skills and connected private sources
   from becoming undisclosed inputs. Record any host injection that cannot be removed.
4. Submit turn-01.txt exactly. Wait for completion before submitting the next
   turn file into the SAME session. Do not combine later user turns into the
   first prompt. Do not coach the agent with expected observations.
5. Save full transcript, command events, host/version/model, outputs and changed
   files after each turn. Keep unknown metadata null. The prompt has an explicit
   AGENTS.md read wrapper; this tests explicit-read adherence, not native discovery.
6. Validate the resulting package and record command output. Compare files to
   before-manifest.json. For FB-03 compare unrelated-sentinel.txt exactly.
7. Complete a COPY of run-record.json and ASSESSMENT.md with observed evidence.
   Hard-stop behaviors make a trial fail even if package validation passes.
8. Keep earlier failures. Repeats and old-guidance comparisons are separate runs
   with their own inputs and evidence. This bundle has one candidate input per
   case and no baseline comparison.

Do not mark preparation, successful process exit or valid files as behavioral pass.
Fresh-context outcomes do not establish learner comprehension or other-host support.

## Preparation evidence

FB-03/preparation-checks.json records successful validation/status and expected
strict-coverage refusal using existing dependencies. The initial missing-dependency
failure is retained in FB-03/dependency-missing-checks.json. It is not an agent failure.
verify.py checks original workspace hashes, prompt presence, explicit not_run state,
FB-01/02 absence of a prebuilt user package and FB-03 initial project state.
Verification makes no model calls or network requests and writes no trial results.

CLI planning references: local codex exec help reported 0.162.0-alpha.17.2.
Official noninteractive execution documentation was inspected at
https://learn.chatgpt.com/docs/non-interactive-mode . No CLI model run occurred.
