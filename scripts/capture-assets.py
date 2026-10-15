#!/usr/bin/env python3
"""Save the public delivered frontend and its declared assets for local review."""
import concurrent.futures
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
ORIGIN = 'https://activetheory.net/'
BUCKET = 'https://storage.googleapis.com/activetheory-v6.appspot.com/'
VERSION = '1780406240914'
records = {}
failures = []

def destination(url):
    if url.startswith(ORIGIN):
        relative = unquote(urlsplit(url).path).lstrip('/') or 'index.html'
    elif url.startswith(BUCKET):
        relative = 'content/' + unquote(urlsplit(url).path).split('.appspot.com/', 1)[1]
    else:
        raise ValueError('Unexpected asset origin: ' + url)
    path = (DIST / relative).resolve()
    if not path.is_relative_to(DIST.resolve()):
        raise ValueError('Invalid asset path')
    return path

def download(url):
    url = url.split('?', 1)[0]
    path = destination(url)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or not path.stat().st_size:
        temporary = path.with_name(path.name + '.download')
        encoded = quote(url, safe=':/%')
        result = subprocess.run(['curl', '-fLsS', '--retry', '2', '--max-time', '150', encoded, '-o', str(temporary)], capture_output=True)
        if result.returncode:
            temporary.unlink(missing_ok=True)
            return {'url': url, 'error': result.stderr.decode().strip()[-250:]}
        temporary.replace(path)
    data = path.read_bytes()
    if path.suffix != '.html' and b'<html' in data[:200].lower():
        path.unlink()
        return {'url': url, 'error': 'Source returned its HTML fallback instead of this asset'}
    return {'url': url, 'path': str(path.relative_to(DIST)), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def batch(urls):
    urls = sorted({unquote(url).split('?', 1)[0] for url in urls} - records.keys())
    print(f'Capturing {len(urls)} assets', flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for index, result in enumerate(pool.map(download, urls), 1):
            if 'error' in result:
                failures.append(result)
            else:
                records[result['url']] = result
            if index % 50 == 0:
                print(f'  {index}/{len(urls)}', flush=True)

def references(text):
    # Only complete, literal paths; dynamic template paths are handled explicitly.
    return {ORIGIN + match for match in re.findall(r'["\'`]((?:assets/)[^"\'`<>\r\n${}]+\.[a-zA-Z0-9]+)["\'`]', text)}

def media_references(value, urls):
    if isinstance(value, dict):
        if value.get('filename') and value.get('prefix') == 'media':
            urls.add(BUCKET + value['prefix'] + '/' + value['filename'])
        for child in value.values():
            media_references(child, urls)
    elif isinstance(value, list):
        for child in value:
            media_references(child, urls)
    elif isinstance(value, str) and value.startswith(BUCKET + 'media/'):
        urls.add(value)

def main():
    initial = [ORIGIN, ORIGIN + f'assets/js/app.{VERSION}.js', ORIGIN + f'assets/js/modules.{VERSION}.js', ORIGIN + f'assets/data/uil.{VERSION}.json']
    initial += [BUCKET + f'cms/{key}-dev.json' for key in ['metadata', 'contact', 'projects']]
    batch(initial)
    reference_app = ROOT / f'reference/assets/js/app.{VERSION}.js'
    app = (reference_app if reference_app.exists() else destination(initial[1])).read_text()
    urls = set(json.loads((ROOT / 'docs/observed-resources.json').read_text()))
    for category, folder in [('GEOMETRIES', 'geometry'), ('TEXTURES', 'images')]:
        body = re.search(r'window.UIL_ASSETS_' + category + r'=\[(.*?)\]', app).group(1)
        urls.update(ORIGIN + f'assets/{folder}/' + path for path in re.findall(r'filename:"([^"]+)"', body))
    sources = list((DIST / 'assets/js').rglob('*.js')) + list((DIST / 'assets/data').glob('*.json')) + list((ROOT / 'reference/content/cms').glob('*.json')) + [DIST / 'index.html']
    for path in sources:
        text = path.read_text()
        urls.update(references(text))
        if path.suffix == '.json':
            try:
                media_references(json.loads(text), urls)
            except json.JSONDecodeError:
                continue
    urls.update(ORIGIN + 'assets/js/lib/' + path for path in ['basis_transcoder.js', 'basis_transcoder.wasm', '_draco/draco_wasm_wrapper.js', '_draco/draco_decoder.wasm', '_draco/draco_decoder.js'])
    for weight in ['Regular', 'Light', 'Bold']:
        urls.update(ORIGIN + f'assets/fonts/NBArchitektStd-{weight}' + ext for ext in ['.png', '.json'])
        urls.update(ORIGIN + f'assets/fonts/NBArchitektStd-{weight}-export/NBArchitektStd-{weight}' + ext for ext in ['.woff2', '.woff', '.otf'])
    urls.add(ORIGIN + 'unsupported.html')
    batch(urls)
    (ROOT / 'docs/asset-manifest.json').write_text(json.dumps({'source': ORIGIN, 'version': VERSION, 'assets': list(records.values()), 'unavailable': failures}, indent=2) + '\n')
    print(f'Saved {len(records)} assets ({sum(r["bytes"] for r in records.values()) / 1024**2:.1f} MiB); {len(failures)} unavailable', flush=True)

if __name__ == '__main__':
    main()
