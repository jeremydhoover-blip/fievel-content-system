"""Build a self-contained Fievel plugin into a NEW directory; no user data copied."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ('WORKFLOW.md', 'HUMAN-REVIEW.md', 'SOURCE-PROVENANCE.md', 'CONSUMER-EXPORT.md')
SCRIPTS = ('fievel.py', 'adapters.py', 'consumer.py', 'provenance.py',
           'review_evidence.py', 'review_page.py', 'viewer.py')
TARGETS = ('codex', 'claude')
SKILLS = ('getting-started', 'content-system-builder', 'source-discovery',
          'ai-behavior-designer', 'evaluation-designer', 'content-audit')


def plugin_skill(canonical, preamble):
    """Insert the plugin path preamble after a canonical skill's frontmatter and title."""
    lines = canonical.splitlines()
    if not lines or lines[0] != '---':
        raise ValueError('Canonical skill lacks frontmatter')
    closing = lines.index('---', 1)
    title = next(i for i in range(closing + 1, len(lines)) if lines[i].startswith('# '))
    combined = lines[:title + 1] + [''] + preamble.splitlines() + lines[title + 1:]
    return ('\n'.join(combined) + '\n').encode('utf-8')


def claude_manifest(source):
    """Derive Claude Code's .claude-plugin/plugin.json from the authored manifest."""
    authored = json.loads(source)
    interface = authored.get('extensions', {}).get('com.openai', {}).get('interface', {})
    manifest = {key: authored[key] for key in ('name', 'version', 'description', 'homepage', 'repository', 'license')}
    if interface.get('developerName'):
        manifest['author'] = {'name': interface['developerName']}
    manifest['keywords'] = ['content-design', 'content-system', 'ai-behavior', 'evaluation']
    # Read only for directory listings; must stay inside the plugin root.
    manifest['icon'] = './assets/fievel-logo.png'
    manifest['documentationUrl'] = authored['repository'] + '#install-as-a-plugin'
    manifest['supportUrl'] = interface['supportURL']
    manifest['privacyPolicyUrl'] = interface['privacyPolicyURL']
    return (json.dumps(manifest, indent=2) + '\n').encode('utf-8')


def package_files(root=ROOT, target='codex'):
    if target not in TARGETS:
        raise ValueError(f'Unknown target: {target}')
    root = Path(root).resolve()
    result = {}

    def read(source):
        source = root / source
        if source.resolve() != source.absolute():
            raise ValueError(f'Redirected package input: {source}')
        return source.read_bytes()

    def add(source, destination):
        result[destination] = read(source)

    if target == 'claude':
        # Claude Code reads its manifest from .claude-plugin/, not the root.
        result['.claude-plugin/plugin.json'] = claude_manifest(read('plugin-src/plugin.json'))
    else:
        add('plugin-src/plugin.json', 'plugin.json')
    preamble = read('plugin-src/skill-preamble.md').decode('utf-8')
    for name in SKILLS:
        result[f'skills/{name}/SKILL.md'] = plugin_skill(read(f'.agents/skills/{name}/SKILL.md').decode('utf-8'), preamble)
    for name in ('AGENTS.md', 'requirements.txt', 'LICENSE', 'VERSION'):
        add(name, f'runtime/{name}')
    for name in DOCS:
        add(f'docs/{name}', f'runtime/docs/{name}')
    for name in SCRIPTS:
        add(f'scripts/{name}', f'runtime/scripts/{name}')
    for folder, suffixes in {
        '.agents/skills': {'.md'}, 'knowledge': {'.md'}, 'schemas': {'.json'},
        'templates/content-system': {'.json'}, 'examples': {'.json', '.md'},
        'viewer': {'.html', '.js', '.css'}, 'review-ui': {'.js', '.css'},
    }.items():
        for path in sorted((root / folder).rglob('*')):
            if path.is_file() and path.suffix in suffixes:
                relative = path.relative_to(root).as_posix()
                add(relative, f'runtime/{relative}')
    add('website/dist/assets/fievel-logo.png', 'assets/fievel-logo.png')
    add('plugin-src/README.md', 'README.md')
    add('LICENSE', 'LICENSE')
    return result


def build(output, root=ROOT, target='codex'):
    files = package_files(root, target)
    output = Path(output).absolute()
    if output.resolve() != output:
        raise ValueError('Redirected output directory')
    # Exclusive creation prevents accidental replacement of a prior candidate.
    output.mkdir(parents=True, exist_ok=False)
    for relative, content in files.items():
        path = output / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    manifest = {name: hashlib.sha256(content).hexdigest() for name, content in sorted(files.items())}
    # Bytes, not text mode: Windows would otherwise write CRLF.
    (output / 'bundle-manifest.json').write_bytes((json.dumps(manifest, indent=2) + '\n').encode('utf-8'))
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    parser.add_argument('--target', choices=TARGETS, default='codex',
                        help='Host plugin format (default: codex)')
    args = parser.parse_args()
    try:
        manifest = build(args.out, target=args.target)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'{exc}\n')
    print(f'Built {len(manifest)} {args.target} files in {args.out}')
