"""Build a self-contained Fievel pilot into a NEW directory; no user data copied."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ('WORKFLOW.md', 'HUMAN-REVIEW.md', 'SOURCE-PROVENANCE.md', 'CONSUMER-EXPORT.md')
SCRIPTS = ('fievel.py', 'adapters.py', 'consumer.py', 'provenance.py',
           'review_evidence.py', 'review_page.py', 'viewer.py')


def package_files(root=ROOT):
    root = Path(root).resolve()
    result = {}

    def add(source, destination):
        source = root / source
        if source.resolve() != source.absolute():
            raise ValueError(f'Redirected package input: {source}')
        result[destination] = source.read_bytes()

    for path in sorted((root / 'plugin-src').rglob('*')):
        if path.is_file():
            add(path.relative_to(root), path.relative_to(root / 'plugin-src').as_posix())
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
    add('LICENSE', 'LICENSE')
    return result


def build(output, root=ROOT):
    files = package_files(root)
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
    (output / 'bundle-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    try:
        manifest = build(args.out)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'{exc}\n')
    print(f'Built {len(manifest)} files in {args.out}')
