# Offline setup verification

The reproducible local check is:

```sh
python scripts/verify_offline_setup.py --out docs/audits/new-offline-setup
```

Choose a new output directory inside the repository. Existing directories are
refused. The script retains a fresh workspace and virtual environment under
.scratch for inspection. It neither deletes existing folders nor activates an agent.
There are no model calls and pip runs with --no-index and --no-cache-dir.

The check creates a venv without system site packages and runs its interpreter
in isolated mode. PYTHONPATH/PYTHONHOME are removed. It tests the missing-validator
message, attempts offline pip installation, and, if no distribution is available,
copies the existing local .deps tree into the fresh workspace. That fallback is
reported explicitly as runtime recovery, not clean installation.

It exercises initialization, strict validation, status, literal checks, evidence
review preparation/validation, incomplete-review refusal, provenance audit,
consumer export, viewer generation, overwrite refusal, adapter integrity and the
full unit suite. It records commands, exits, stdout/stderr, local dependency hashes
and runtime metadata. The fictional workflow uses the fixed project-review date
2026-10-21 and is not a current organizational freshness assessment.

## What the observed run establishes

See audits/2026-10-21/offline-setup-final for the successful final run and earlier
offline-setup-local-temp for preserved failures. The initial sandbox temp path
blocked ensurepip; a workspace-local temporary directory resolved that. The first
clean-copy unit suite found tests relying on an existing .scratch directory; test
setup now creates it explicitly.

No package wheel was available to satisfy requirements through offline pip. The
successful runtime workflow therefore depends on a copied existing installation.
It is Windows/Python-specific, including the installed rpds binary. This is not
proof that another machine can install from requirements or that macOS/Linux works.

## Remaining installation evidence

A clean dependency installation needs an authorized package download or an approved
local wheelhouse. Then repeat in a new environment with the exact distributions,
record transitive versions and hashes and check supported Python/platform versions.
Do not infer native skill activation from adapter file equality. That remains a
separate host test. Retained scratch workspaces may be removed later after reviewing
the saved evidence, but this script performs no recursive deletion.
