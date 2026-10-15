# Inspection and verification

Reference: https://activetheory.net/, October 15, 2026. Delivered build identifier: `1780406240914`.

## Observed reference behavior

REA scenario evidence `ev_9a59dbd4f3164025cf24d52c6c2d5d624c6722c61ae900d0661b4703885302ef` captured the original home scene at 1440 × 900, its DOM/accessibility tree, and 140 distinct request URLs. No JavaScript page errors were recorded in that finite scenario. The entire visual experience is rendered through a canvas, with a hidden accessibility tree and DOM chat/video elements.

Browser-harness was used through an isolated Chrome CDP session to exercise the real reference. Work moves the scroll position to the gallery and changes the path to `/work`. Selecting a card opens `/work/<slug>` with video and project details. Contact opens the full-screen glass/globe overlay while retaining the underlying route. The original front page shuffles its project cards; lights, particles, pointer response, music order, and video frames vary over time.

Reference screenshots: `reference-home.png`, `reference-work.png`, `reference-detail.png`, and `reference-contact.png`.

## Local implementation

953 public frontend files were retained, totaling approximately 1.09 GiB. These include all 351 geometry/texture files declared by the shipped renderer, 15 font files, eight music tracks, and all 547 media URL references in the captured 65-project CMS data. The delivered renderer is retained; it is not a clean-room source reconstruction.

REA passive inspection evidence `ev_d503377d6c6e6eb16983d23891066a8272ece16ac49f36e697ef0f0968f5a833` observed the local canvas, accessibility structure, scripts, and video elements. Its attach-window and origin-filter limits are retained in `rea-evidence.json`.

Browser-harness confirmed the following local interactions at 1440 × 900:

- Home renders the animated logo, ribbon, particles, jellyfish, and top navigation.
- Work moves to the card gallery and `/work`.
- A card opens project details and its local video. The video reached `HAVE_ENOUGH_DATA` (`readyState = 4`).
- Contact opens and closes the glass/globe overlay with its original typography and destinations.
- Entering `Show Kandinsky` in the chat field navigates to the captured project slug `/work/kaninsky-vr`, displays the local description, and re-enables the input.
- The checked main-frame resource lists contained no external resource requests or HTTP failures.

Responsive home rendering was inspected at 375 × 812 with mobile emulation, 768 × 1024, 1280 × 800, and 1440 × 900. These are browser emulation checks rather than physical-device certification.

Wheel scrolling was also exercised beyond the project gallery into the Lab section and final scene. The retained network event window contained canceled media requests during navigation, with no JavaScript exceptions or HTTP failures observed in that window. This event window is bounded; it is not a full execution trace of every possible interaction.

`npm run verify` passes six groups covering all declared geometry/texture file sizes, all project media references, the limited renderer URL replacements, history routes, HEAD/404 behavior, byte-range video delivery, and the complete local search request sequence. See `browser-checks.json`, `mobile-check.json`, and `responsive-checks.json` for captured states.

## Remaining differences and limits

The original private AI backend is not accessible as source. Its API has a local project-search adapter, which does not reproduce generative AI answers. QR mobile synchronization has its original interface but no recreated local synchronization backend. Original outbound links remain unchanged. Analytics were removed, and region detection uses a local India fixture.

Eleven literal paths embedded in the original HTML or bundle already return HTML fallback pages instead of assets on the original host. Those responses were excluded rather than saved as corrupt image/script files; their exact paths appear under `unavailable` in `asset-manifest.json`. All graphics files declared in the asset manifests and all project media references used by the local CMS are present.

The original unminified project source, unpublished assets, and private infrastructure have not been recovered. No exhaustive pixel or behavioral equality claim is made. The saved runtime evidence and visual comparisons cover the listed states; animated frames vary with timing, randomness, and the device GPU.
