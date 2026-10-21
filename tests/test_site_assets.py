from pathlib import Path
import re
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.stamp_site_assets import ASSETS, SITE, stamp

class SiteAssetStampTests(unittest.TestCase):
    def test_every_page_links_current_asset_stamps(self):
        for page in sorted(SITE.glob('*.html')):
            text=page.read_text(encoding='utf-8')
            for name in ASSETS:
                for link in re.findall(r'\./'+re.escape(name)+r'[^"]*',text):
                    self.assertEqual(link,f'./{name}?v={stamp(name)}',f'{page.name}: run python scripts/stamp_site_assets.py')

    def test_pages_link_the_stylesheet(self):
        for page in sorted(SITE.glob('*.html')):
            self.assertIn(f'./styles.css?v={stamp("styles.css")}',page.read_text(encoding='utf-8'),page.name)

if __name__=='__main__':
    unittest.main()
