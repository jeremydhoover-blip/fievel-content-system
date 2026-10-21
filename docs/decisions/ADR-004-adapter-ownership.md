# ADR 004 Generated adapter ownership

Date: 2026-10-21
Scope: WP-05 and F-05

Use a versioned .claude/fievel-adapters.json manifest recording generated relative
paths and last-written SHA-256 hashes. sync --check detects missing, changed and
retired generated files. sync refuses stale files and locally modified managed
outputs before writing anything. It never deletes files or directories.

When canonical skills are renamed or removed, the manifest keeps their previous
paths visible until the user moves or removes the retired copies. An absent
retired file can be dropped from the manifest on the next successful sync.
Unrelated files are not adopted, changed or deleted. Existing expected files may
be adopted at first migration only when identical to current canonical output.
Existing root adapters also require exact equality during adoption. Conflicting
unowned expected paths are errors, not permission to overwrite.

A missing manifest requires sync migration; --check cannot claim full ownership
verification. Older orphan skills from before the manifest cannot be reliably
identified and are left alone. Do not infer ownership from directory location or
frontmatter names. Document this migration limit. Manifest paths are limited to
the generated output locations; redirected/symlink paths are rejected.

Sync preflights conflicts before writes, but is not a transaction against concurrent
filesystem edits or disk failure. Concurrent sync/edit operations are unsupported.
Generated hashes are ownership bookkeeping, not authentication or a security signature.
Host discovery and model behavior remain separately untested.
