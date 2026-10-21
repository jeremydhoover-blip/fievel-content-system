# Offline setup results

Date: 2026-10-21
Platform: Windows 11, Python 3.12.10
Scope: TR-01/02/07/08 and EX-07; no model calls or package downloads

Created a separate workspace and venv without system site packages. Isolated-mode
commands did not inherit PYTHONPATH/PYTHONHOME. Missing jsonschema produced the
expected installation instruction. Offline pip (--no-index --no-cache-dir) could
not find jsonschema 4.26.0; installation is NOT verified.

Copied the existing local dependency installation into the fresh workspace as a
separately identified recovery path. Recorded versions and file hashes. After that,
all CLI exercise steps passed: initialization, validation, status, literal checks,
evidence review and incomplete refusal, provenance, export, viewer, overwrite
refusal and adapter integrity. All 78 tests passed in the isolated venv.

Failures are preserved: sandbox temporary-folder permissions blocked ensurepip in
offline-setup-retry/setup-failure.json. A workspace-local temporary directory fixed
bootstrap. The first complete workflow under offline-setup-local-temp found 14 test
errors because adapter/consumer tests assumed .scratch existed. Test setup now
creates it explicitly, including the standalone malformed-input suite. The final
fresh-copy run has no unexpected failures. No production feature change required.

This verifies local runtime recovery from installed dependencies on this one
Windows/Python environment. It does not verify pip installation, dependency
availability on another machine, native host activation or other platforms.
Next installation gate needs an authorized distribution download or local wheelhouse.
Human calibration and agent/consumer behavior remain open; no model calls occurred.
