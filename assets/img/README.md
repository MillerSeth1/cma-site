# Images

**Logo** (built from Seth's master `Copper_Mountain_Air_Logo.svg` by `tools/make_logo.py`; only the artwork inside the master's page was used, Inkscape workspace extras dropped):
- `logo-light.svg` / `logo-dark.svg`: horizontal lockup (mark + wordmark) for dark / light backgrounds. Header uses light.
- `logo-stacked-light.svg` / `logo-stacked-dark.svg`: the original stacked logo. Footer and share image use light.
- `logo-mark-*.svg`: mark only. `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`: mark on a dark tile.
- `og-image.jpg`: 1200×630 share image (`tools/make_png.py`).

**Photos** live in `photos/` as `<slot>-<width>.{avif,webp,jpg}`, made by `tools/optimize_images.py` from originals that stay OUTSIDE this repo (`/workspace/cma-website/photos/` on the box). Outputs are cropped, resized, converted to sRGB and saved with no EXIF/GPS/ICC metadata. Alt text lives in `IMG` in `tools/build.py`.

To change a photo: edit the slot's source in `tools/optimize_images.py`, rerun it, rebuild. Never use `staff/` (team page on hold) or `_not-for-web/`.

| Slot | Source | Used on |
|---|---|---|
| hero | aircraft/Cessna414A_DSC09602 | Home hero |
| ramp-band | aircraft/Cessna414A_DSC09616 | Home full-width band; share image |
| terminal | aircraft/Cessna414A_DSC09575 | About; KOLS guide draft |
| fbo | aircraft/Hangar_with_the_Hangar_Queen | Home card, Services FBO, Fuel & FBO |
| cargo | kols/KOLS_2026-10-21_06 | Home cargo card |
| cargo-sign | kols/KOLS_2026-10-21_01 | Services cargo; cargo draft |
| kols-guide | kols/KOLS_2026-10-21_03 | KOLS guide draft; blog empty state |
| training | kols/KOLS_2026-10-21_05 | Flight Training, coming-soon sections |
| charter | lighting/KOLS_lighting_fullsizerender | Charter |
| community, event, ww-* | wings-and-wheels/* | About (Community); Wings & Wheels draft |
| fuel | `fuel.svg` placeholder (no fuel photo yet) | Fuel cards/sections |
