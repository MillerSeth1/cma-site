# Copper Mountain Air website (preview)

Static site for Copper Mountain Air, LLC at Nogales International Airport (KOLS), Nogales, AZ.

- **Preview:** https://millerseth1.github.io/cma-site/ (noindex, robots Disallow — preview only)
- **Hosting:** GitHub Pages (free), built by GitHub Actions from `tools/build.py` on every push to `main`.
- **No custom domain yet.** There is intentionally no `CNAME` file. Do not add one, and do not change DNS: `coppermountainair.com` carries Microsoft 365 email (MX, autodiscover, SPF/DKIM/DMARC and related records). The domain switch waits for Seth's approval.

## Layout

| Path | What it is |
|---|---|
| `tools/build.py` | Page templates, nav, SEO/JSON-LD, image slot map. Builds into `_site/`. |
| `posts/` | Blog posts as Markdown with front matter. `_TEMPLATE.md` is the starting point. |
| `assets/css`, `assets/js`, `assets/fonts` | Styles, small script (nav, reveal motion, contact form), self-hosted Archivo + Inter (SIL OFL). |
| `assets/img/` | Logo variants, favicons, share image, and optimized photos (`photos/`, AVIF/WebP/JPEG, no metadata). Originals stay outside the repo. See `assets/img/README.md`. |
| `tools/optimize_images.py`, `tools/make_logo.py`, `tools/make_png.py`, `tools/make_art.py` | Rebuild photos, logo SVGs, favicons/OG image, and the remaining fuel placeholder. |

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

## Going live later (needs Seth's approval)

1. Set `PREVIEW = False` and `SITE_URL` to the real domain in `tools/build.py` (removes noindex, opens robots.txt).
2. Add the custom domain in repo Settings → Pages, and add **only** the website records at the DNS host (an `A`/`CNAME` for `www` and the apex). Leave every Microsoft 365 record (MX, autodiscover CNAME, SPF TXT, DKIM selector CNAMEs, DMARC, any `msoid`/`lyncdiscover`/SRV records) untouched.

## Unlisted preview pages

For a post Seth wants to see on the live preview without listing it: keep `published: false` and add `unlisted: true`, `unlisted_token: <random 10+ lowercase letters/digits>` and optionally `unlisted_file: <name>`. It renders only at `preview/<token>/<name>.html`, is never added to the blog index, home, nav or sitemap, and always carries noindex. Ordinary `published: false` drafts still never render. Note the repo is public, so the text and token are readable on GitHub.
