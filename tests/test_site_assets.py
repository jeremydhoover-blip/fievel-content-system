from pathlib import Path
import json
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

class SiteDiscoveryTests(unittest.TestCase):
    def test_crawlers_find_every_page(self):
        robots=(SITE/'robots.txt').read_text(encoding='utf-8')
        self.assertIn('Sitemap: https://fievel.ai/sitemap.xml',robots)
        listed=set(re.findall(r'<loc>https://fievel\.ai/([^<]*)</loc>',(SITE/'sitemap.xml').read_text(encoding='utf-8')))
        self.assertEqual(listed,{'' if p.name=='index.html' else p.name for p in SITE.glob('*.html')})

    def test_pages_name_their_canonical_address(self):
        for page in SITE.glob('*.html'):
            address='https://fievel.ai/'+('' if page.name=='index.html' else page.name)
            self.assertIn(f'<link rel="canonical" href="{address}">',page.read_text(encoding='utf-8'),page.name)

    def test_structured_data_matches_the_release(self):
        html=(SITE/'index.html').read_text(encoding='utf-8')
        data=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',html,re.S).group(1))
        self.assertEqual(data['@type'],'SoftwareApplication')
        self.assertEqual(data['softwareVersion'],(ROOT/'VERSION').read_text(encoding='utf-8').strip())

    def test_llms_txt_points_to_the_site(self):
        text=(SITE/'llms.txt').read_text(encoding='utf-8')
        self.assertEqual(text.splitlines()[0],'# Fievel')
        self.assertIn('https://fievel.ai/',text)

if __name__=='__main__':
    unittest.main()
