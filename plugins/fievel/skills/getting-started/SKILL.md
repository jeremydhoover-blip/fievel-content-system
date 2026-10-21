---
name: getting-started
description: Start or resume Fievel onboarding and choose a beginner, existing-guidelines, or AI-experience workflow.
---

# Getting Started

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

Read AGENTS.md and docs/WORKFLOW.md. If a project exists, read its progress.json
and validate it before asking for information again. Briefly summarize the saved
decisions, open questions, and next stage. Do not re-onboard an experienced user.

For a new user, introduce Fievel as an AI content systems architect, then offer:
“I’m new to this”, “I have existing content guidelines”, or “I’m building an AI
experience”. Ask which path fits. Explain that a content system connects product
context, rules, sources, behavior, checks, and ownership. Offer the Wayfarer example
without requiring company data. Ask one useful question at a time and say why.

Use knowledge/INDEX.md to load one relevant local explanation; fundamental concepts
and the fictional exercise should not depend on web requests. If the user asks how
the parts connect, read knowledge/content-design/system-relationships.md. If they
ask how another AI uses the files, read knowledge/ai-fundamentals/instructions-and-skills.md.
After the first useful saved artifact, offer a local overview using
`python scripts/fievel.py view <folder> --out <new.html>`. It works with partial
drafts, displays diagnostics, and does not edit files. It is a snapshot: regenerate
after edits using a new filename. Do not describe it as live sync or automatic
consumer integration. Do not load execution reports unless the user selects one.

Create a NEW folder with `python scripts/fievel.py init my-content-system` (add
`--example` only if the user chooses fictional practice). Record path and explanation
preference in progress.json. For existing guidelines ask for their approved local
location; discovery does not authorize ingestion or external access. Experienced
users can skip lessons and supply a product brief directly.

Output: project folder and saved next_action, decisions, open_questions. Check:
the user understands what will be created; no private sources copied without scope.
Recovery: if the destination exists, resume it or choose a new name; never replace it.
Example: “I’m new” -> offer Wayfarer -> stage 1, one product task.
