# Adapter maintenance

Fievel keeps canonical skills in .agents/skills and generated Claude copies in
.claude/skills. CLAUDE.md and .github/copilot-instructions.md are generated too.

```sh
python scripts/fievel.py sync
python scripts/fievel.py sync --check
```

The versioned .claude/fievel-adapters.json manifest records owned paths and hashes
of their normalized UTF-8 text. Keep it with the repository. Do not edit it to hide
a conflict. It is bookkeeping, not an authenticated ownership signature.

## Normal edits

Edit canonical guidance, then sync. Unmodified generated copies update. --check
reports missing or changed outputs and differing recorded hashes. Missing generated
copies can be restored by sync. It does not remove any files or directories.

## Renames and removals

After a canonical skill is renamed or removed, an existing old generated copy is
reported as stale by both sync and --check. Sync stops before updating other files.
Inspect it and preserve local edits. Move the retired skill outside the agent's
skill discovery directories, or explicitly remove the copy yourself, then sync
again. An absent retired file is dropped from the next successful manifest.
Do not delete every unexpected skill directory: it may contain unrelated user work.

## Local edits and conflicts

If an owned copy differs from its last written version and from current canonical
output, sync refuses to overwrite it. Preserve and reconcile the changes manually,
put intended Fievel changes in the canonical file, then rerun sync. Existing unowned
files at required output paths must exactly match expected generated content before
adoption. Otherwise sync reports an unowned-path conflict without writing outputs.
Unknown paths elsewhere are not adopted or touched.

## First migration

An old installation with no manifest must run sync. Identical expected copies are
adopted; different copies need manual reconciliation. --check reports the missing
manifest rather than claiming ownership has been verified. Pre-manifest orphan
skills cannot reliably be distinguished from user skills, so they are left alone.
A successful migration does not certify that no historic orphan exists. Review
older installations manually if a skill was retired before migration.

## Boundaries

Manifest paths are limited to generated locations. Redirected paths are rejected.
All ownership/conflict checks happen before writes, but sync is not transactional
against disk failure or concurrent editors. Run one sync at a time. These checks
verify local files; native skill discovery and behavior in each agent host still
require separate execution evidence.
