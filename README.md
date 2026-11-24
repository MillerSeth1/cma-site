# Copper Mountain Air website

Static site for Copper Mountain Air, LLC at Nogales International Airport (KOLS), Nogales, AZ.

- **Live site:** https://coppermountainair.com/
- **Hosting:** GitHub Pages, built by GitHub Actions from `tools/build.py` on every push to `main`.
- **DNS caution:** Point only the website records (apex `A`/`AAAA` and `www`) at GitHub Pages. Leave every Microsoft 365 email record untouched: MX, `autodiscover` CNAME, SPF/DKIM/DMARC TXT, `lyncdiscover`/`sip` CNAMEs, and related SRV records.

## Layout

| Path | What it is |
|---|---|
| `tools/build.py` | Page templates, nav, SEO/JSON-LD, image slot map. Builds into `_site/`. |
| `posts/` | Blog posts as Markdown with front matter. `_TEMPLATE.md` is the starting point. |
| `gallery.html` | Photo gallery (built by `tools/build.py` from `assets/img/gallery/`). |
| `weather.html` | Live KOLS weather, radar and VFR climatology (built by `tools/build.py`). |
| `assets/css`, `assets/js`, `assets/fonts` | Styles, small script (nav, reveal motion, contact form), self-hosted Archivo + Inter (SIL OFL). |
| `assets/img/` | Logo variants, favicons, share image, and optimized photos (`photos/`, AVIF/WebP/JPEG, no metadata). Originals stay outside the repo. See `assets/img/README.md`. |
| `tools/optimize_images.py`, `tools/make_logo.py`, `tools/make_png.py`, `tools/make_art.py` | Rebuild photos, logo SVGs, favicons/OG image, and the remaining fuel placeholder. |

Spanish pages live under `/es/` (for example `_site/es/index.html` and `https://coppermountainair.com/es/`). Every public page has an EN | ES toggle, `hreflang` alternates, and a matching sitemap entry. Page bodies for Spanish are in `tools/pages_es.py`; translated blog posts go in `posts/es/` with the same slug as the English post. Aviation terms that pilots use in both languages (VFR, NOTAM, METAR, 100LL, Jet A, CTAF, ASOS, VOR/DME) are kept as-is. Widgets pick up Spanish UI labels from `document.documentElement.lang`.

Build locally: `pip install markdown && python3 tools/build.py` then open `_site/index.html`.
Public contact details (address, phone, hours, after-hours fueling, amenities and payment cards) live as constants near the top of `tools/build.py`. Do not invent facts; confirm any new detail before adding it.

## HOW TO ADD A POST (one new post a month)

1. Copy `posts/_TEMPLATE.md` to `posts/DRAFT-YYYY-MM-short-slug.md`.
2. Fill in the front matter and write the post. Keep `published: false`.
3. Commit and push. **Drafts never render on the site**: the deploy build skips every post whose front matter isn't `published: true`.
4. **Review:** build locally with drafts shown, for review only:
   `python3 tools/build.py --drafts && open _site/blog/index.html` (never deploy this build), or read the Markdown on GitHub.
5. **Approval step:** Seth reads the draft and replies with approval. Nothing is published without that explicit OK.
6. To publish after approval: set `published: true`, set `date:` to the real publish date, clear every `[PLACEHOLDER]`, and rename the file to drop the `DRAFT-` prefix (`posts/YYYY-MM-short-slug.md`). Commit with a message like `Publish: <title> (approved by Seth YYYY-MM-DD)` and push. The Action rebuilds and deploys in about a minute.
7. To unpublish, set `published: false` and push.

Note: this repo is public (required for free GitHub Pages), so draft Markdown is readable on GitHub even though it is not on the site.

## Production settings

`tools/build.py` is set to production: `PREVIEW = False` and `SITE_URL = "https://coppermountainair.com/"`. Public pages are indexable; `robots.txt` allows crawlers and disallows `/preview/`. The build writes `_site/CNAME` with `coppermountainair.com` for GitHub Pages.

To temporarily return to a noindex preview build, set `PREVIEW = True` and restore `SITE_URL` to the github.io preview URL. Do not change Microsoft 365 DNS records when updating website records at GoDaddy.

## Unlisted preview pages

For a post Seth wants to see on the live preview without listing it: keep `published: false` and add `unlisted: true`, `unlisted_token: <random 10+ lowercase letters/digits>` and optionally `unlisted_file: <name>`. It renders only at `preview/<token>/<name>.html`, is never added to the blog index, home, nav or sitemap, and always carries noindex. Ordinary `published: false` drafts still never render. Note the repo is public, so the text and token are readable on GitHub.
