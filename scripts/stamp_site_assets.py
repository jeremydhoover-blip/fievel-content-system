"""Stamp website asset links with a content hash so browsers never pair a new page with a cached old stylesheet or script.

Run after editing website/dist/styles.css or main.js:
    python scripts/stamp_site_assets.py
Pass --check to fail instead of writing when a stamp is out of date.
"""
import hashlib
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / 'website' / 'dist'
ASSETS = ('styles.css', 'main.js')


def stamp(name):
    return hashlib.sha256((SITE / name).read_bytes()).hexdigest()[:10]


def main(check=False):
    stale = []
    for page in sorted(SITE.glob('*.html')):
        text = page.read_text(encoding='utf-8')
        updated = text
        for name in ASSETS:
            pattern = re.compile(r'(\./' + re.escape(name) + r')(\?v=[0-9a-f]+)?(?=")')
            updated = pattern.sub(lambda m, n=name: f'{m.group(1)}?v={stamp(n)}', updated)
        if updated != text:
            stale.append(page.name)
            if not check:
                page.write_text(updated, encoding='utf-8', newline='\n')
    if check and stale:
        print('Out of date asset stamps in: ' + ', '.join(stale) + '. Run python scripts/stamp_site_assets.py')
        return 1
    print(('Checked' if check else 'Stamped') + ' asset links in ' + str(len(list(SITE.glob('*.html')))) + ' pages')
    return 0


if __name__ == '__main__':
    sys.exit(main(check='--check' in sys.argv[1:]))
