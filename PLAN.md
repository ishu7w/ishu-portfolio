# Ishu Patel portfolio personalization plan

Status: implemented. See `docs/personalization-verification.md` for completed checks and operating scope.

## Goal and audience

Turn the existing local WebGL experience into Ishu Patel's portfolio for internships, recruiters, and project/open-source collaborators. Preserve its scene composition, shader materials, camera paths, scroll transitions, typography, spacing, and interaction timing. Change identity, copy, links, project imagery and data, search content, and brand marks.

## Content sources and boundaries

- Authenticated GitHub connector confirms account `ishu7w`, name Ishu Patel, and the public contact address already published on the profile.
- Public profile README establishes Computer Science & Engineering student, Java/data structures, full-stack software, applied AI, and open-source Java work.
- Current repository READMEs take precedence over older profile summaries, particularly for Parkwise and Credence.
- Featured original projects: Parkwise, Credence, Scholarship & Aid, SmartHealth, CINEMATIC, and ScholarAI.
- Separately labelled open-source contribution cards: Checkstyle, Gson, and Java Pathfinder, using verified pull request descriptions and links.
- LinkedIn and LeetCode use the user's exact profile destinations, with tracking parameters removed from LinkedIn. No unverified college, employer, graduation date, rank, solved count, awards, or client claims.
- Only public repository material is used in the website. Private repositories are excluded.

## Page mapping

| Existing surface | Personalized content | Visual behavior |
| --- | --- | --- |
| Home | Ishu Patel / scroll to explore; personal monogram | Original logo material, ring/ribbon motion, particles and jellyfish |
| About | Code / Build / Improve; student introduction, tools, internship/collaboration interests | Original three-line heading, copy placement and transitions |
| Work gallery | Six original projects plus three labelled contributions | Original floating cards, glass, hover, scroll and detail transition |
| Project detail | What it does, stack, verified scope, source and live preview links | Original video plane, typewriter copy and close interaction |
| Filters | Full stack, Java, AI, creative web, open source | Original positions and animated filtering |
| Lab | Build log / GitHub; learning, experiments and contribution work | Original hexagonal panels, hover and outward navigation |
| Contact | Java / Web / AI; email, GitHub, LinkedIn, LeetCode | Original glass overlay, globe, arrows, social positions and glitches |
| QR | GitHub profile QR | Original QR position; remove the remote mobile-sync claim |
| Metadata | Ishu Patel title, description, social preview and favicon | Original typography and theme |

## Implementation

1. Save verified source references and the above mapping before content edits.
2. Create `content/portfolio.json` as the single editable source for identity, bio, links, categories, projects and contributions. Keep technical scene settings separate.
3. Add a repeatable build step that generates the compatible CMS documents and applies explicit content replacements to the retained bundle. Preserve original snapshots for reproducibility.
4. Capture real public project previews where available. Create clearly identified project/contribution title artwork and short motion reels for the existing media planes; never display Active Theory's client work as Ishu's projects.
5. Replace the agency monogram/texture content while retaining the existing shaders, rings, camera movement and animation envelope.
6. Retarget local search to the personal project set and provide factual biography/skills/contact responses. Preserve the animated frontend interface; no external AI service or credentials are needed.
7. Remove agency social/careers/newsletter/client destinations from the active experience and replace them with useful personal destinations.

## Architecture

`Verified public GitHub sources → content/portfolio.json → build-personalization.py → existing WebGL bundle + local CMS + project media`

`Browser → existing same-origin Node static server → local portfolio-search adapter`

Keep the existing dependency-free Node server and original WebGL runtime. No database or account system is needed for this portfolio. The search API uses one stateless `/api/search` request and reads the generated personal project data. This also supports Vercel serverless deployment.

## Acceptance checks

- Every active page, card, metadata field and search response describes Ishu or a correctly credited public contribution.
- No original agency project media or agency contact destinations are used by the personalized runtime.
- Project source/demo/profile links resolve to verified destinations.
- Core shader files, camera paths, scene transforms and animation values remain unchanged except the identity geometry and text/media references.
- Browser QA: home, About, gallery, category filtering, project details, playable media, source/demo links, Contact, QR destination, Lab and portfolio search.
- Responsive QA at 375, 768 and 1280 pixels, plus desktop comparison screenshots.
- Automated checks validate generated data, replacement coverage, media existence, routes, byte ranges and personal search behavior.
- Keep the local preview running for the user's next review. GitHub and Vercel publication are covered by the subsequently authorized deployment step in `docs/deployment.md`.
