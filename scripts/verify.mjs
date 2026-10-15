import assert from 'node:assert/strict';
import { readFile, stat, access } from 'node:fs/promises';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const root = fileURLToPath(new URL('../', import.meta.url));
const dist = resolve(root, 'dist');
const base = process.env.BASE_URL || `http://127.0.0.1:${process.env.PORT || 4173}`;
let checks = 0;
function pass(message) { checks++; console.log(`PASS ${message}`); }

const original = await readFile(resolve(root, 'reference/assets/js/app.1780406240914.js'), 'utf8');
let graphics = 0;
for (const [category, folder] of [['GEOMETRIES', 'geometry'], ['TEXTURES', 'images']]) {
  const body = original.match(new RegExp(`window.UIL_ASSETS_${category}=\\[(.*?)\\]`))[1];
  for (const match of body.matchAll(/filename:"([^"]+)",bytes:(\d+)/g)) {
    const info = await stat(resolve(dist, 'assets', folder, match[1]));
    assert.equal(info.size, Number(match[2]), match[1]);
    graphics++;
  }
}
pass(`${graphics} original model and texture file sizes match the delivered manifests`);

const projects = JSON.parse(await readFile(resolve(dist, 'content/cms/projects-dev.json'), 'utf8'));
const paths = new Set();
function collect(value) {
  if (typeof value === 'string' && (value.startsWith('/content/') || value.startsWith('assets/images/personal/'))) paths.add('/' + decodeURIComponent(value.split('?')[0]).replace(/^\//, ''));
  else if (Array.isArray(value)) value.forEach(collect);
  else if (value && typeof value === 'object') Object.values(value).forEach(collect);
}
collect(projects);
for (const path of paths) await access(resolve(dist, '.' + path));
const profile = JSON.parse(await readFile(resolve(root, 'content/portfolio.json'), 'utf8'));
assert.equal(projects.length, profile.projects.length);
assert.equal(projects.filter(project => project.period === 'Merged contribution').length, 3);
for (const project of projects) {
  assert.ok(project.video.url.startsWith('/content/portfolio/'));
  assert.ok(project.video.thumbnail.startsWith('assets/images/personal/'));
  assert.ok(project.caseStudyURL.startsWith('https://github.com/'));
}
pass(`All ${paths.size} CMS media references for ${projects.length} projects exist locally`);

const localized = await readFile(resolve(dist, 'assets/js/app.1780406240914.js'), 'utf8');
for (const forbidden of ['Active Theory', 'HELLO@ACTIVETHEORY.NET', 'mailto:hello@activetheory.net', 'https://atlab.io', 'Im trained on 112', 'https://mailchi.mp/activetheory', 'https://jobs.lever.co/activetheory']) assert.ok(!localized.includes(forbidden), forbidden);
const before = JSON.parse(await readFile(resolve(root, 'reference/assets/data/uil.1780406240914.json'), 'utf8'));
const after = JSON.parse(await readFile(resolve(dist, 'assets/data/uil.1780406240914.json'), 'utf8'));
const changes = JSON.parse(await readFile(resolve(root, 'docs/personalization-patches.json'), 'utf8'));
let changed = 0;
for (const [key, value] of Object.entries(before)) {
  if (JSON.stringify(value) === JSON.stringify(after[key])) continue;
  changed++;
  assert.ok(changes.scene_content_keys.includes(key) || after[key]?.src?.includes('/personal/ishu-logo') || ['assets/images/personal/lab-mark.png','assets/images/personal/lab-map.png'].includes(after[key]?.src), `Unexpected scene change: ${key}`);
}
const manifest = JSON.parse(await readFile(resolve(root, 'docs/asset-manifest.json'), 'utf8'));
const shader = manifest.assets.find(asset => asset.path === 'assets/shaders/compiled.vs');
assert.equal(createHash('sha256').update(await readFile(resolve(dist, shader.path))).digest('hex'), shader.sha256);
pass(`Shaders remain identical; ${changed} scene changes are limited to text and identity references`);

for (const route of ['/', '/work', ...projects.map(project => `/work/${project.slug}`)]) {
  const response = await fetch(base + route);
  assert.equal(response.status, 200);
  const markup = await response.text();
  assert.match(markup, /<title>Ishu Patel/);
  assert.ok(!markup.includes('Active Theory'));
}
assert.equal((await fetch(base + '/assets/missing-file.png')).status, 404);
assert.equal((await fetch(base + '/assets/js/app.1780406240914.js', { method: 'HEAD' })).status, 200);
assert.equal((await fetch(base + '//assets/images/personal/github.png')).status, 200);
pass('Home, Work, project history routes, HEAD, and missing-file handling');

const fallback = await (await fetch(base + '/unsupported.html')).text();
assert.match(fallback, /<title>Ishu Patel/);
assert.equal((fallback.match(/<article>/g) || []).length, projects.length);
for (const forbidden of ['googletagmanager.com', 'gtag(', 'Active Theory']) assert.ok(!fallback.includes(forbidden));
for (const project of projects) assert.ok(fallback.includes(project.caseStudyURL));
pass('Unsupported-browser fallback contains every personal project and no inherited analytics');

const videoPath = '/content/portfolio/parkwise.mp4';
const response = await fetch(base + videoPath, { headers: { Range: 'bytes=0-1023' } });
assert.equal(response.status, 206);
assert.equal((await response.arrayBuffer()).byteLength, 1024);
assert.match(response.headers.get('content-range'), /^bytes 0-1023\/\d+$/);
assert.equal((await fetch(base + videoPath, { headers: { Range: 'bytes=999999999999-' } })).status, 416);
const suffix = await fetch(base + videoPath, { headers: { Range: 'bytes=-128' } });
assert.equal(suffix.status, 206);
assert.equal((await suffix.arrayBuffer()).byteLength, 128);
pass('Video byte ranges, suffix ranges, and invalid ranges');

async function post(message) {
  const response = await fetch(`${base}/api/search`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message }) });
  assert.equal(response.status, 200);
  return response.json();
}
for (const project of projects) assert.equal((await post(project.name)).slug, project.slug);
assert.equal((await post("I'm looking at parkwise. Show Credence")).slug, 'credence');
for (const [query, expected] of [['Who is Ishu?', /Ishu Patel/], ['What are your skills?', /Java.*TypeScript/], ['Contact', /ishu7w@gmail.com/], ['internships', /internships/]]) {
  const result = await post(query);
  assert.equal(result.slug, '');
  assert.match(result.text, expected);
}
assert.equal((await fetch(`${base}/api/search`)).status, 405);
for (const message of ['', 'x'.repeat(2001), null]) {
  assert.equal((await fetch(`${base}/api/search`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message }) })).status, 400);
}
assert.equal((await fetch(`${base}/api/search`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{' })).status, 400);
pass('Stateless search for every project, context changes, biography, skills and contact; invalid requests rejected');
console.log(`\n${checks} verification groups passed.`);
