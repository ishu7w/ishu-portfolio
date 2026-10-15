# Ishu Patel — immersive developer portfolio

A personal portfolio for internships, software projects, open-source work, and collaborators. It preserves the retained WebGL experience's materials, particles, camera movement, scroll transitions and typography, with Ishu's identity and content throughout.

Live: [ishu-portfolio-six.vercel.app](https://ishu-portfolio-six.vercel.app/) · [GitHub repository](https://github.com/ishu7w/ishu-portfolio)

## Run

Requires Node.js 24 and Python 3 for the content build. No npm dependencies are needed for the portfolio server.

```sh
npm start
```

Open http://127.0.0.1:4173/. Set `PORT` to use another port. The server binds to loopback by default.

## Customize

Edit `content/portfolio.json`, then run:

```sh
npm run build
```

Restart `npm start` after changing project or biography data so the local conversation adapter reads the new content. Text fields, project order, descriptions, categories, skills, contact details and destinations live in that JSON file. Project identifiers must be unique. The active media files are under `dist/content/portfolio/`; thumbnails and logo textures are copied to `dist/assets/images/personal/` by the build.

Six original projects are featured: Parkwise, Credence, Scholarship & Aid, SmartHealth, CINEMATIC and ScholarAI. Three cards separately credit merged contributions to Checkstyle, Gson and Java Pathfinder. Only verified public GitHub material is used. LinkedIn and LeetCode are linked without unverified statistics or biography details.

The two working hosted previews captured for artwork are Parkwise and Credence. Other projects and contribution cards use editorial title artwork. Videos are short motion presentations of those screenshots/title cards, not recorded demonstrations of application workflows.

## Structure

- `PLAN.md`: audience, source policy, content mapping, implementation and acceptance plan.
- `content/portfolio.json`: editable personal content.
- `scripts/build-personalization.py`: reproducible content, metadata and identity build.
- `scripts/runtime_patches.py`: checked rendering, search, keyboard and video fixes; generated personal fallback.
- `scripts/branding_geometry.py`: IP monogram meshes, retaining the original circular frame.
- `scripts/portfolio-search.mjs`: factual local biography, skills, contact and project responses.
- `scripts/server.mjs`: static files, history routes, byte-range media serving, and the conversation API.
- `dist/assets/data/uil.1780406240914.json`: original scene configuration with only content and identity references replaced.
- `dist/assets/shaders/compiled.vs`: unchanged retained shader collection.
- `dist/content/cms/`: generated personal project, contact and metadata documents.
- `dist/content/portfolio/media-sources.json`: artwork sources and video verification.
- `docs/github-public-sources.json` and `docs/contribution-sources.json`: public README snapshots and verified PR records.
- `reference/`: preserved reference HTML, bundle, CMS and scene data used by the build.

## Verify

Run the server, then:

```sh
npm run verify
```

Checks cover the unsupported-browser fallback, retained geometry and texture sizes, every active project media reference, unchanged shaders and scene transforms, personal identity coverage, all project routes, video byte ranges, and the full local search request sequence. Browser checks cover the rendered portfolio and responsive states; see `docs/personalization-verification.md`.

The conversation UI uses deterministic local lookup, with no external AI account required. The QR points to the public GitHub profile. Analytics have been removed. The production deployment serves the committed `dist/` on Vercel. Search uses one stateless `/api/search` request, so it works across serverless cold starts. See `docs/deployment.md` for publishing and checks.

## Reference provenance

The visual/runtime foundation was captured from https://activetheory.net/ on October 15, 2026, delivered build `1780406240914`. Its original unminified source and private infrastructure were not recovered. Original source snapshots and earlier inspection notes remain for reproducibility; active portfolio content is generated separately. `scripts/localize.py` is the baseline localization helper called by the personal build, while `npm run localize` runs the complete personal build.

## Rights and reuse

Public visibility does not prevent cloning or forking. Ishu's original content, artwork and integration code are all rights reserved under `LICENSE`. The retained Active Theory runtime, fonts, music, textures and other third-party material are excluded; their owners retain their rights, and this repository does not supply a reuse license for them. See `THIRD_PARTY_NOTICES.md` for provenance.

## Runtime performance and bug fixes

Rendering uses a consistent, bounded pixel ratio for the scene and final canvas. The card shaders cache their shared refraction object instead of requesting it every frame. The fullscreen player loads on demand and suspends background GPU drawing while open. Search times out after eight seconds, clears pending loading animations, and always re-enables input. Filters support keyboard activation; video dialogs support Escape and restore focus. A generated HTML portfolio remains available on browsers without WebGL, with no analytics. See `docs/runtime-performance.md` for measurements and regression checks.
