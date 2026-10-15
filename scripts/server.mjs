import http from 'node:http';
import { createReadStream } from 'node:fs';
import { readFile, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import search from '../api/search.mjs';

const root = fileURLToPath(new URL('../dist/', import.meta.url));
const host = process.env.HOST || '127.0.0.1';
const port = Number(process.env.PORT || 4173);
const types = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8', '.json': 'application/json', '.css': 'text/css', '.wasm': 'application/wasm', '.woff': 'font/woff', '.woff2': 'font/woff2', '.otf': 'font/otf', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.gif': 'image/gif', '.svg': 'image/svg+xml', '.mp4': 'video/mp4', '.mp3': 'audio/mpeg', '.bin': 'application/octet-stream', '.ktx2': 'image/ktx2', '.vs': 'text/plain' };
const projects = JSON.parse(await readFile(resolve(root, 'content/cms/projects-dev.json'), 'utf8'));
const profile = JSON.parse(await readFile(resolve(root, 'content/portfolio/profile.json'), 'utf8'));

function json(res, status, value) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
  res.end(JSON.stringify(value));
}

const server = http.createServer(async (req, res) => {
  try {
    const pathname = decodeURIComponent(new URL('http://localhost' + (req.url.startsWith('/') ? req.url : '/' + req.url)).pathname);
    if (pathname === '/api/search') return await search(req, res);
    if (pathname === '/health') return json(res, 200, { ok: true, projects: projects.length });
    if (!['GET', 'HEAD'].includes(req.method)) return json(res, 405, { error: 'Method not allowed' });
    let path = resolve(root, '.' + pathname);
    if (path !== root.slice(0, -1) && !path.startsWith(root.endsWith(sep) ? root : root + sep)) return json(res, 403, { error: 'Invalid path' });
    let info;
    try { info = await stat(path); }
    catch {
      if (!extname(pathname) && !pathname.startsWith('/assets/') && !pathname.startsWith('/content/')) {
        path = resolve(root, 'index.html');
        info = await stat(path);
      } else return json(res, 404, { error: 'File not found', path: pathname });
    }
    if (info.isDirectory()) { path = resolve(path, 'index.html'); info = await stat(path); }
    const headers = { 'Content-Type': types[extname(path)] || 'application/octet-stream', 'Accept-Ranges': 'bytes', 'Cache-Control': 'no-cache', 'X-Content-Type-Options': 'nosniff' };
    let start = 0, end = info.size - 1, status = 200;
    if (req.headers.range) {
      const match = /^bytes=(\d*)-(\d*)$/.exec(req.headers.range);
      if (!match || (!match[1] && !match[2])) { res.writeHead(416, { 'Content-Range': `bytes */${info.size}` }); return res.end(); }
      if (!match[1]) start = Math.max(0, info.size - Number(match[2]));
      else { start = Number(match[1]); if (match[2]) end = Math.min(end, Number(match[2])); }
      if (start > end || start >= info.size) { res.writeHead(416, { 'Content-Range': `bytes */${info.size}` }); return res.end(); }
      status = 206;
      headers['Content-Range'] = `bytes ${start}-${end}/${info.size}`;
    }
    headers['Content-Length'] = Math.max(0, end - start + 1);
    res.writeHead(status, headers);
    if (req.method === 'HEAD' || info.size === 0) return res.end();
    const stream = createReadStream(path, { start, end });
    stream.on('error', () => res.destroy());
    res.on('close', () => stream.destroy());
    stream.pipe(res);
  } catch (error) {
    if (!res.headersSent) json(res, error.status || (error instanceof URIError ? 400 : 500), { error: error.status ? error.message : 'Request failed' });
    else res.destroy();
  }
});

server.listen(port, host, () => console.log(`Local: http://${host}:${port}`));
for (const signal of ['SIGINT', 'SIGTERM']) process.on(signal, () => server.close(() => process.exit(0)));
