---
name: content-audit
description: Audit an existing Fievel package for gaps, contradictory rules, source problems and evaluation coverage.
---

# Content Audit

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

Read AGENTS.md. Required input: selected project folder and audit scope. Run
`python scripts/fievel.py validate <folder>` and `status` first. Uncovered draft
rules are reported as work remaining; run validate with --require-coverage when
assessing evaluation preparation, not ordinary early-stage draft integrity. Review source
authority/freshness, competing rules, approval status, missing context and ownership.
Check that scenarios cover actual tasks and failure situations, not just literal
phrases. Compare result system_sha256 with current package before drawing conclusions.

Output: a new audit Markdown file separating observed issues, uncertainties and
suggested changes, with rule/source IDs and supporting evidence. Do not edit rules
as part of a read-only audit. Prioritize findings by their effect on user tasks.
If validation fails, report exact errors and continue any possible read-only review.
Example: unknown policy date -> freshness gap, not proof the policy is wrong.
