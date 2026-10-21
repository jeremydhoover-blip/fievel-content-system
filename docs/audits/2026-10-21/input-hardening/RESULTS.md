# Input hardening results

Date: 2026-10-21
Scope: invalid local JSON and safe report preparation; TR-05/06/07 and EX-07

Preserved failing probes in before.txt. Six initial tests reported twelve failing
subtests/assertions: duplicate keys, nonfinite numbers, encoding diagnostics,
serialization side effects and nesting handling. No model calls were made.

Shared JSON loading now rejects duplicate keys (including nested objects), NaN,
Infinity, overflowing numeric exponents and unpaired Unicode surrogates. Errors
identify the input path. UTF-8 BOM, valid Unicode, false and null field values stay
supported. A 128-level JSON nesting limit produces a clear input error rather than
runtime-dependent recursion behavior. The viewer uses the same parser and labels
bad sections as diagnostics; adapter manifests also use the strict parser.

Report serialization/UTF-8 encoding completes before creating parent directories
or opening the exclusively new output. Unserializable values, invalid numbers or
Unicode cannot leave an empty report. Existing output refusal remains intact.
Explicit null provenance input is rejected rather than treated as omitted.

Seven new tests bring the suite from 65 to 72 passing. Eight adapter checks pass.
The CLI malformed-input tests cover evidence review, review validation and source
provenance; tests compare input/output preservation. Logs include first, intermediate
and final runs. The initial nesting expectation exposed runtime variation; an
explicit limit repaired the contract. No universal malformed-input coverage claimed.

Compatibility: previously tolerated ambiguous/nonstandard JSON is now rejected.
No package/report schema or existing valid data was migrated. Human judgment,
source truth, clean installs and model behavior remain unverified.

Limits: these changes do not guarantee bounded memory for arbitrarily large files,
atomicity under disk failure, or correctness for every possible malformed input.
Next offline work: a reviewed consumer export contract with explicit draft/approved
selection, provenance and action boundaries; actual AI adherence remains untested.
