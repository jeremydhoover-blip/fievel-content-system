# Claude Code plugin pilot

2026-10-21. Local build only, not a public release. No Claude Code session has
installed or run this bundle yet; everything below is file-format and unit-test
evidence. Formats were checked against the Claude Code
[plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference) and
[marketplace](https://code.claude.com/docs/en/plugins/marketplace-reference) references.

## Package design

The Claude bundle is built from the same `plugin-src/` and runtime sources as the
[Codex pilot](CODEX-PLUGIN-PILOT.md). Its skill and `runtime/` bytes are identical;
only the manifest differs:

| | Codex (`plugins/fievel`) | Claude Code (`plugins/fievel-claude`) |
| --- | --- | --- |
| Manifest | root `plugin.json` (authored) | `.claude-plugin/plugin.json` (derived) |
| Catalog | `.agents/plugins/marketplace.json` | `.claude-plugin/marketplace.json` |
| Installed identity | `fievel@fievel-content-system` | `fievel@fievel-content-system` |

The derived manifest keeps name, version, description, license and author, and
adds keywords and an `icon` (read only by directory listings). The Codex-only
`extensions` block is not copied. Both bundles carry the same six skills; each
skill's preamble locates `runtime/` two directories above its own SKILL.md,
which holds in both installed layouts.
Python 3.10+ and jsonschema remain separate prerequisites, as for Codex.

## Build and refresh

```sh
python scripts/build_plugin.py --target claude --out plugins/fievel-claude-next
```

`--target codex` remains the default. Output folders must be new. To refresh the
committed bundle, remove `plugins/fievel-claude`, rebuild it there and run the
tests: `test_committed_bundles_match_fresh_builds` fails when either committed
bundle no longer matches its sources. Never hand-edit a bundle.

## First trial (not yet run)

Requires a `claude` CLI, which was not available when this bundle was built.

```sh
claude plugin validate plugins/fievel-claude --strict
claude plugin marketplace add ./
claude plugin install fievel@fievel-content-system
```

Validate the plugin directory itself: validating a marketplace does not open the
plugins it lists. Then open a fresh Claude Code session in a separate workspace
and follow the trial tasks in [CODEX-PLUGIN-PILOT.md](CODEX-PLUGIN-PILOT.md#first-human-trial).
Record host version, outcome and friction the same way. A successful install
does not prove skill invocation, setup, resume or adherence.
