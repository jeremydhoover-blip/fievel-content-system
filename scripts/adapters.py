"""Conservative generated-adapter bookkeeping; never deletes user files."""
import hashlib
import json
from pathlib import Path, PurePosixPath
from .fievel import read


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def safe_path(root, relative):
    if not isinstance(relative, str):
        raise ValueError('Adapter manifest path must be text')
    parts = PurePosixPath(relative).parts
    allowed = relative in ('CLAUDE.md', '.github/copilot-instructions.md', '.claude/fievel-adapters.json')
    allowed = allowed or (len(parts) == 4 and parts[:2] == ('.claude', 'skills') and
                          parts[3] == 'SKILL.md' and parts[2] not in ('.', '..'))
    if not allowed or '\\' in relative or ':' in relative or '..' in parts:
        raise ValueError(f'Unsafe adapter path: {relative}')
    path = root / relative
    if path.resolve() != path.absolute():
        raise ValueError(f'Redirected adapter path: {relative}')
    return path


def sync_adapters(root, check=False):
    root = Path(root).resolve()
    expected = {}
    for source in sorted((root / '.agents/skills').glob('*/SKILL.md')):
        if source.resolve() != source.absolute():
            raise ValueError('Redirected canonical skill path')
        expected[f'.claude/skills/{source.parent.name}/SKILL.md'] = source.read_text(encoding='utf-8')
    for relative in ('CLAUDE.md', '.github/copilot-instructions.md'):
        expected[relative] = '# Fievel adapter\n\nRead and follow `AGENTS.md` at the repository root.\nCanonical workflows live in `.agents/skills/`.\nDo not edit this generated adapter; run `python scripts/fievel.py sync`.\n'
    manifest_path = safe_path(root, '.claude/fievel-adapters.json')
    previous = {}
    if manifest_path.exists():
        manifest = read(manifest_path)
        if not isinstance(manifest, dict) or set(manifest) != {'version', 'files'} or manifest['version'] != '1.0' or not isinstance(manifest['files'], dict):
            raise ValueError('Unsupported adapter manifest')
        previous = manifest['files']
        for relative, fingerprint in previous.items():
            safe_path(root, relative)
            if relative == '.claude/fievel-adapters.json' or not isinstance(fingerprint, str) or len(fingerprint) != 64 or any(c not in '0123456789abcdef' for c in fingerprint):
                raise ValueError('Invalid adapter manifest entry')
    elif check:
        raise ValueError('Adapter ownership manifest missing; run sync to migrate identical existing copies')
    problems = []
    for relative in sorted(set(previous) - set(expected)):
        path = safe_path(root, relative)
        if path.exists():
            problems.append(f'Stale generated adapter: {relative}; preserve or remove it manually before sync')
    for relative, text in expected.items():
        path = safe_path(root, relative)
        existing = path.read_text(encoding='utf-8') if path.exists() else None
        if existing is not None and existing != text:
            if relative not in previous:
                problems.append(f'Unowned adapter conflict: {relative}')
            elif digest(existing) != previous[relative]:
                problems.append(f'Locally modified generated adapter: {relative}')
        if check and (existing != text or previous.get(relative) != digest(text)):
            problems.append(f'Adapter drift: {relative}')
    if problems:
        raise ValueError('\n'.join(problems))
    if not check:
        # Full conflict preflight above; no recursive cleanup or deletion.
        for relative, text in expected.items():
            path = safe_path(root, relative)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8', newline='\n')
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps({'version':'1.0', 'files':{r:digest(t) for r,t in expected.items()}}, indent=2) + '\n', encoding='utf-8')
    return len(expected)
