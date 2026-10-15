# Rendering and interaction fixes

This update keeps the scene configuration, camera paths, shaders, materials, particle counts, content, and animation timing. Changes live in `scripts/runtime_patches.py` and the personalization builder, so rebuilding does not erase them. Every replacement checks that the expected source occurs exactly once.

## Rendering

The retained renderer used its own pixel-ratio calculation for the final canvas, independently of `World.DPR`. On the tested high-density desktop this produced a 2560 × 1600 output while scene targets used a lower ratio. Under Android emulation, scene targets used DPR 1 while the final canvas used DPR 2.

The final canvas now uses `World.DPR`. Scene resolution respects the physical display ratio, caps DPR at 1.5, and uses a two-million-pixel desktop / one-million-pixel mobile budget with a 0.75 floor for very large viewports. This intentionally trades excess supersampling for smoother rendering. It does not remove effects or reduce particle counts.

At 1280 × 800 CSS pixels with DPR 2, canvas pixels decreased from 4,096,000 to 1,998,984, approximately **51% fewer**. At 390 × 844 with Android / DPR 3 emulation, they decreased from 1,316,640 to 329,160, **75% fewer**. Warm frame samples after the update were approximately 60 FPS in both checks. These are isolated Chrome checks on an Apple M4, with an emulated phone; they are not physical Android measurements or a guarantee for every device.

Work-card refraction objects are acquired once, rather than creating async lookups on every render frame. Phone layout uniforms update on resize. The native fullscreen video player has no source until opened, avoiding a duplicate showreel load during startup. While a project video is open, GPU drawing behind the dialog stops; the clock, DOM events and native player remain active, and scene drawing resumes on close.

## Interaction fixes

- Search aborts after eight seconds, clears its loading animations, and re-enables input on success or failure. Input is disabled immediately, rather than in a delayed fade callback. A controlled immediate-response test passed both before and after the change; the original timing path was hardened rather than treated as a reliably reproduced lockup.
- The inherited recording disclaimer was replaced with factual portfolio-search copy.
- Filters now have keyboard focus and support Enter / Space activation without changing the page hash.
- Video dialogs have a label, Escape dismissal, focus restoration, inline playback support and handled playback rejections. Closing pauses the native video. The selected project's source is preserved between opens.
- The unsupported-browser page now contains Ishu's profile, verified links and all nine projects. Original Google Analytics was removed. Disabling WebGL led to this fallback automatically, without horizontal overflow on the emulated phone.
- Social preview image URLs are absolute, and font loading uses `font-display: swap`.

## Verification

`PORT=4175 npm run verify` passed seven groups: graphics integrity; nine-project media; unchanged shaders and allowed scene edits; application routes; personal fallback with no inherited analytics; video ranges; and factual search / invalid inputs. JavaScript syntax, Python compilation and `git diff --check` passed.

Browser regression checks covered immediate search responses, recovery from a deliberately hung request, filtering by keyboard, searching for Parkwise after filtering, the selected project video, Escape dismissal, paused hidden media, zero background renderer calls while the dialog was open, and resumed rendering after dismissal. Desktop and mobile captures preserved the composition. Bounded event windows reported no JavaScript exceptions. Metrics and results are recorded in `runtime-performance.json`.

The mechanical UI scan reported one warning for the existing Helvetica fallback in the JavaScript-disabled notice. The portfolio continues to use the retained NB Architekt font; no typography redesign was introduced.
