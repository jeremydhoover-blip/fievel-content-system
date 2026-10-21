---
name: ai-behavior-designer
description: Define AI responsibilities, permissions, uncertainty and recovery rules for a Fievel content system.
---

# AI Behavior Designer

## Using this skill from the Fievel plugin

This plugin carries Fievel's workflows and Python tools. The user's project is
separate from the installed plugin. Find the plugin root two directories above
this SKILL.md; its `runtime/` directory is the bundled resource root, called R below.
Resolve R from this skill's actual installed path, never a development checkout.

- Prefer Fievel's MCP tools when they are available (names start with `fievel_`).
  Local tools such as `fievel_init`, `fievel_validate`, `fievel_check` and
  `fievel_view` work only inside the user's workspace and never overwrite files;
  call `fievel_setup_status` first. Remote tools such as `fievel_validate_package`
  and `fievel_check_responses` receive package content, store nothing, and return
  results to save as new files; tell the user that content is sent to the Fievel
  server for processing. Without tools, use the CLI as described below.
- Read `R/AGENTS.md` for Fievel's conversation and workflow rules. References in
  this skill and in AGENTS.md to AGENTS.md, docs/, knowledge/, templates/, examples/,
  schemas/, scripts/ and .agents/skills/ are relative to R, not the user's working directory.
- Keep the current working directory in the user's chosen workspace. Run the CLI
  by its absolute path: `python "R/scripts/fievel.py" <command> <project> ...`.
  Replace R with the resolved path. Resolve project and output paths in the user's
  workspace. Run one simple command per step: the Python interpreter
  with the CLI path and its arguments, without chained commands, shell variables
  or PowerShell scripts. Read and list files with the host's file tools. Simple
  commands keep the user's permission prompts clear and predictable. Never create
  projects, install dependencies, or edit inside R or the plugin cache. Never copy Fievel AGENTS.md over a user's repository instructions.
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

Read AGENTS.md and stage 4 of docs/WORKFLOW.md. Required inputs: product tasks,
actual available tools and the selected project's standards/sources. Ask what the
assistant should explain versus act on. Read knowledge/ai-experience-design/behavior.md
when explanation is useful. Define responsibility boundaries, clarification triggers,
confirmation for consequential actions, uncertainty, recovery and human handoff.

Write behavior.json with stable rule IDs and source links. Tool availability must
be verified; intended integrations are not working tools. The Wayfarer assistant
has no action tools, so must never claim to change or cancel bookings. Personalization
must use only provided context. Never infer hidden account information.

Output: draft behavior rules, linked human or deterministic checks in evaluation.json,
saved decisions/progress. Validate the package. If permissions are unclear, keep the
action unavailable and identify the decision needed. Example: “cancel now” with no
tool -> explain the limitation and give the booking confirmation next step.
