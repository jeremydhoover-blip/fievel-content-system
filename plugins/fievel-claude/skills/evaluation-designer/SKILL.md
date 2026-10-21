---
name: evaluation-designer
description: Create plain-language Fievel quality checks, check saved responses, or prepare human review without claiming unexecuted tests ran.
---

# Evaluation Designer

## Using this skill from the Fievel plugin

This plugin carries Fievel's workflows and Python tools. The user's project is
separate from the installed plugin. Find the plugin root two directories above
this SKILL.md; its `runtime/` directory is the bundled resource root, called R below.
Resolve R from this skill's actual installed path, never a development checkout.

- Read `R/AGENTS.md` for Fievel's conversation and workflow rules. References in
  this skill and in AGENTS.md to AGENTS.md, docs/, knowledge/, templates/, examples/,
  schemas/, scripts/ and .agents/skills/ are relative to R, not the user's working directory.
- Keep the current working directory in the user's chosen workspace. Run the CLI
  by its absolute path: `python "R/scripts/fievel.py" <command> <project> ...`.
  Replace R with the resolved path. Resolve project and output paths in the user's
  workspace. Run one simple command per step: the Python interpreter
  with the CLI path and its arguments, without chained commands, shell variables
  or PowerShell scripts. Read and list files with the host's file tools. Simple
  commands keep the user's permission prompts clear and predictable. Never create projects, install dependencies, or edit inside R or the
  plugin cache. Never copy Fievel AGENTS.md over a user's repository instructions.
- Check Python 3.10+ and `python -c "import jsonschema"`. If missing, explain the
  prerequisite. When setup is authorized, create a new `.fievel-venv` in the user's
  workspace and install `R/requirements.txt` with its Python. Reuse a working
  environment; do not overwrite an existing environment. Use that interpreter for
  every CLI command. Do not install globally or claim the plugin bundles Python.
- Follow existing workspace instructions. Explain that project files remain local,
  but material read into the conversation is handled by the user's coding agent.
- The repository-maintenance and adapter-sync instructions in R/AGENTS.md are for
  Fievel development, not for modifying the installed plugin during a user session.
- Other Fievel skills in this plugin: getting-started, content-system-builder,
  source-discovery, ai-behavior-designer, evaluation-designer and content-audit.
  Switch to the one that fits when the user's request changes.

Save projects under the user's chosen folder (default `my-content-system/` in
their workspace). The user approves content; validation does not. Do not run
model evaluations unless the user authorized them.

## Workflow

Read AGENTS.md and stages 5–6 of docs/WORKFLOW.md. Required inputs: actual design
requirements, realistic user situations and a project folder. Read
knowledge/evaluations/checking-quality.md on demand. Translate “good” into inspectable
questions; link each check's requirement_id to a standards or behavior rule.
Cover ordinary, unknown, conflicting-source and action-request situations.

Use contains/not_contains only for case-insensitive literal checks. Use human for
meaning, invented facts, tone, accessibility and action authorization. A phrase
absence cannot prove the absence of unauthorized action. Store definitions in
evaluation.json. Drafts can be saved before coverage is complete; before execution,
run `python scripts/fievel.py validate <folder> --require-coverage` and address
uncovered requirements. With no saved responses, explain that checks are defined,
not run.

To inspect a real saved execution report alongside the package, generate
`python scripts/fievel.py view <folder> --report <execution.json> --out <new.html>`.
The viewer reproduces literal outcomes before presenting totals, and marks stale,
unsupported or altered reports. It does not validate completed human judgments
or establish the origin of saved responses. Do not equate reproduced with approved.

With actual saved text mapped by scenario ID, run:
`python scripts/fievel.py check <folder> --responses <json> --out <new-report.json>`.
Prepare a separate review using `review` with the same arguments. Human questions
stay not_run in execution and pending in the review sheet. The reviewer records
identity, date, pass/fail and rationale; never fabricate completed human judgments.
For a self-contained evidence review, read docs/HUMAN-REVIEW.md. Use
`review <folder> --responses <json> --evidence-config <config> --out <new.json>`.
The configuration supplies draft/reviewed rubrics, explicit source excerpts and
response origins; never invent approved criteria or fetch source locations implicitly.
`validate-review <report> --require-complete` checks completed records; add
`--folder <folder>` to reject staleness. Missing responses remain not_run; pending,
borderline and insufficient_evidence cannot count as complete. A complete record
can contain failures and is not content approval or authenticated human authorship.
Legacy sheets must be regenerated in the opt-in format rather than relabeled.

AI judgments, if requested conversationally, must be labeled AI suggestions and
stored separately; no judge backend is implemented.

Output: definitions, actual report if executed, pending review, suggested improvements
in a separate Markdown note. Compare hashes before reusing results after edits.
Recovery: no responses or unknown IDs -> repair the mapping, never substitute fixtures
as evidence about a live agent. Example: “Don’t invent decline reasons” -> human check.
