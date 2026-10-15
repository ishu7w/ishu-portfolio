# Ishu Patel portfolio — verification

Personalization completed on October 15, 2026 for the user's chosen audiences: internships/recruiters and project collaborators.

## Content and sources

The authenticated GitHub account is `ishu7w` / Ishu Patel. The site uses only public repository material. Six original projects are featured, alongside three separately labelled merged contributions verified through the upstream pull-request APIs. README snapshots and PR author/merge records are retained in `github-public-sources.json` and `contribution-sources.json`.

LinkedIn and LeetCode destinations are exactly the user-supplied profiles, with LinkedIn tracking parameters removed. Their public content was inaccessible to the fetch tools, so no education dates, institution, ratings, rankings or solved counts were inferred.

Current project README content takes precedence over the older GitHub profile summary. Parkwise and Credence have captured working public previews. Scholarship & Aid's hosted deployment remained on a loading overlay during inspection, so its card offers source without a live-preview claim.

## Preserved visual behavior

The shader collection is byte-identical to the captured reference. All 351 original geometry/texture files remain intact. The build creates new IP monogram geometry and changes only text and identity/media references in the active scene configuration. Camera paths, scene transforms, material parameters, particles, timing and scroll transitions are retained. The original social icon positions now display GitHub, LinkedIn and LeetCode. QR points to the verified public GitHub profile.

An inherited path normalization issue in the local static server was fixed, and UI images now follow the renderer's asset path convention. The social textures were checked at their actual 64 × 64 dimensions, rather than accepting a rendered fallback texture. Contact controls also have explicit accessible labels.

## Automated checks

`npm run verify` passes six groups:

1. All 351 retained graphics files match the delivered size manifests.
2. All 27 project logo/thumbnail/video references exist locally, and the nine cards have personal source links and media.
3. Shader hashes remain unchanged; scene differences are restricted to content and identity references; agency identity and contact destinations are absent from the active bundle.
4. Home, gallery and all nine detail routes serve Ishu's metadata. HEAD, missing-file and duplicate-slash asset routes behave correctly.
5. Media supports ordinary, suffix and invalid byte-range requests.
6. All nine project names resolve through the complete conversation API sequence. Context switching, biography, skills, contact and internship answers use personal content.

Node syntax checks and Python compilation checks pass for the edited scripts and generated bundle. The build is repeatable from the preserved reference snapshots and editable `content/portfolio.json`.

## Browser checks

Browser-harness was used through an isolated Chrome session to verify:

- Home: Ishu's title, personal identity and IP monogram in the retained reflective ring/ribbon scene.
- About: Code / Build / Improve and the verified student biography.
- Gallery and details: nine personal project/contribution cards; project-specific videos load to readyState 4; source/demo links match the selected project.
- Open-source filtering: exactly Checkstyle, Gson and Java Pathfinder remain.
- Search: entering Show Parkwise after filtering opens `/work/parkwise`, displays the correct source and live-preview links and re-enables input.
- Fullscreen media: the labelled video control opens the selected Parkwise video at readyState 4 and the close control dismisses it. This also verifies that fullscreen uses the selected project's media rather than the general showreel.
- Contact: JAVA / WEB / AI, personal email, repository/contribution destinations and correct GitHub/LinkedIn/LeetCode icons. Accessible labels name the contact actions.
- Lab: Build Log copy, a small personal IP emblem using the original logo texture proportions, and personal project imagery replace the agency lab content. The outbound destination is the public repository list.
- Responsive rendering: 375 × 812 with mobile/touch emulation, 768 × 1024 and 1280 × 800, plus 1440 × 900 desktop inspection. Mobile Contact fits the original stacked layout.
- Finite event windows around the inspected flows reported no JavaScript exceptions or HTTP failure responses. These bounded checks do not establish exhaustive browser/device compatibility.

Screenshots named `personalized-*.png` record the inspected states. Media sources and encoding checks are in `dist/content/portfolio/media-sources.json`.

## Operating scope

The animated conversation interface is backed by factual local search, not a hosted generative model. The portfolio stores no GitHub credentials and requires no external AI key. The media loops are animated presentations of actual screenshots or labelled editorial artwork, not recorded application workflows.

This is a local portfolio build. No GitHub repository was created, no commit was made and no public deployment was performed. Original reference files and historical inspection notes remain for reproducibility; they are not the active portfolio content.
