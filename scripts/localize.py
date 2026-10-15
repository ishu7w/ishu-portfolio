#!/usr/bin/env python3
"""Apply explicit local hosting changes without rewriting the WebGL renderer."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
SOURCE = ROOT / 'reference'
BUCKET = 'https://storage.googleapis.com/activetheory-v6.appspot.com/'
VERSION = '1780406240914'

html = (SOURCE / 'index.html').read_text()
html = re.sub(r'\s*<script async src="https://www.googletagmanager.com/gtag/js\?id=[^"]+"></script>', '', html)
html = re.sub(r'\s*<script>\s*window.dataLayer[\s\S]*?</script>', '', html)
html = re.sub(r'\s*<link href="https://activetheory.net" rel="canonical">', '', html)
html = html.replace(BUCKET, '/content/')
(DIST / 'index.html').write_text(html)

app_source = SOURCE / f'assets/js/app.{VERSION}.js'
app = app_source.read_text().replace(BUCKET, '/content/')
app = app.replace('https://us-central1-at-services.cloudfunctions.net/geo', '/content/geo.json')
app = app.replace('https://backend-dot-activetheory-v6.uc.r.appspot.com/api/assistant', '/api/assistant')
(DIST / f'assets/js/app.{VERSION}.js').write_text(app)

for original in (SOURCE / 'content/cms').glob('*.json'):
    (DIST / 'content/cms' / original.name).write_text(original.read_text().replace(BUCKET, '/content/'))
(DIST / 'content/geo.json').write_text(json.dumps({'location': {'countryCode': 'IN'}}) + '\n')
(ROOT / 'docs/local-changes.json').write_text(json.dumps({
    'version': VERSION,
    'changes': [
        'Public asset URLs and CMS media use /content/ on this server.',
        'Google Analytics script and configuration removed from the HTML.',
        'Original domain canonical tag removed from local HTML.',
        'Cookie-region lookup uses a local India region fixture.',
        'Private assistant endpoint uses the local project-search adapter.'
    ],
    'unchanged': ['WebGL renderer', 'shaders', 'scene data', 'geometry', 'fonts', 'navigation', 'animations', 'project content', 'outbound links']
}, indent=2) + '\n')
print('Localized HTML, renderer URLs, CMS files, region lookup, and assistant endpoint.')
