import { readFileSync } from 'node:fs';
import { searchPortfolio } from '../scripts/portfolio-search.mjs';

const profile = JSON.parse(readFileSync(new URL('../content/portfolio.json', import.meta.url), 'utf8'));
const projects = JSON.parse(readFileSync(new URL('../dist/content/cms/projects-dev.json', import.meta.url), 'utf8'));

// Each search is independent so cold starts and concurrent Vercel instances
// cannot lose a visitor's message. Project context travels with the query.
export default async function search(req, res) {
  const reply = (status, value) => {
    res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
    res.end(JSON.stringify(value));
  };
  if (req.method !== 'POST') return reply(405, { error: 'Use POST' });
  try {
    let data = req.body;
    if (data === undefined) {
      let raw = '';
      for await (const chunk of req) {
        raw += chunk;
        if (Buffer.byteLength(raw) > 8192) return reply(413, { error: 'Request too large' });
      }
      data = raw ? JSON.parse(raw) : {};
    } else if (typeof data === 'string') data = JSON.parse(data);
    if (typeof data?.message !== 'string' || !data.message.trim() || data.message.length > 2000) {
      return reply(400, { error: 'Message must contain between 1 and 2000 characters' });
    }
    return reply(200, searchPortfolio(data.message, profile, projects));
  } catch (error) {
    return reply(error instanceof SyntaxError ? 400 : 500, { error: error instanceof SyntaxError ? 'Invalid JSON' : 'Search unavailable' });
  }
}
