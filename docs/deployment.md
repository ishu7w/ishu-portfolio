# Publishing and verification

- Public repository: https://github.com/ishu7w/ishu-portfolio
- Production site: https://ishu-portfolio-six.vercel.app/
- Vercel project: `ishu-portfolio` in `ishu7w-4139s-projects`
- Connected production branch: `main`; pushes deploy automatically.

The public repository uses an all-rights-reserved notice for Ishu's original work, with explicit third-party exclusions. Public GitHub repositories can be cloned and forked; no technical copy prevention is claimed.

Vercel serves the committed `dist/` directory. The Python personalization build runs locally with `npm run build`; commit its generated files before pushing. Vercel intentionally skips rebuilding the captured runtime. Node.js 24 runs `api/search.mjs`, which answers each query independently without sessions, credentials, or a database. Work detail routes rewrite to the application shell; assets and media retain native file handling and range requests.

Unused original agency project videos, the original agency showreel, local screenshots, credentials, and local Vercel configuration are excluded from publication. Runtime geometry and textures are retained for visual fidelity. Git-based deployment avoids the Vercel Hobby CLI's 100 MB source-upload limit.

Local verification: `PORT=4174 npm run verify`, with the local server running on that port. Production verification: `BASE_URL=https://YOUR-DOMAIN npm run verify`. Checks cover retained asset integrity, nine personal project/contribution cards, preserved scene/shader values, routes, video byte ranges, factual stateless search, and invalid API requests.

## Completed production checks

All six automated verification groups passed against the public production domain, including all nine project searches, invalid inputs, direct project routes and video range requests. A real Chrome browser rendered the personal IP monogram, animated home scene and project gallery on the production domain. The production Vercel build was Ready and the repository visibility was verified as public.
