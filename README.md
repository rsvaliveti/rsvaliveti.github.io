# Radhakrishna Valiveti's Personal website

The personal/academic website of Radhakrishna Valiveti, built with the
[Zola](https://www.getzola.org) static site generator and
[Bulma](https://bulma.io) (loaded from a pinned CDN).

I had previously experimented with two zola sites based on these themes:
kodama, zola-academic. Since then I have made changes so that my website 
is completely standalone, i.e., independent of any themes.

## Architecture at a glance

- **Content is data, not markup.** The homepage, experience, education, and
  awards all come from a single `data/cv.yaml`. Publications and patents come
  from `data/papers.bib` / `data/patents.bib`.
- **Publications are real pages.** `scripts/import_bibtex.py` turns each BibTeX
  entry into a Zola content bundle (`content/publications/<slug>/index.md` plus a
  `cite.bib`). This gives every paper/patent a permalink, a detail page with its
  BibTeX, and inclusion in the search index.
- **No theme, no submodule, no SASS build.** The only runtime dependency is the
  CDN stylesheet pinned in `config.toml` (`extra.bulma_version`). Python is only
  needed to (re)generate bundles when the `.bib` files change — never to build.

## Directory structure

```
config.toml                 # site config, nav menu, pinned Bulma version
data/
  cv.yaml                   # single source of truth for the CV
  papers.bib, patents.bib   # publication sources
content/
  _index.md                 # About (home)
  experience/ education/    # CV sections (data-driven)
  publications/ patents/    # _index.md + generated <slug>/ bundles
  search/                   # search page
templates/
  base.html                 # layout: nav, footer, SEO/OG, favicon, JS
  index.html experience.html education.html
  publications.html patents.html publication-page.html
  search.html 404.html
  macros/pub.html           # publication card + type-label macros
static/
  css/custom.css  js/main.js js/search.js  favicon.svg
  icons/                    # local SVG icons (About page social links)
scripts/import_bibtex.py    # BibTeX -> content bundles (dev only)
Makefile  pyproject.toml    # tooling
.github/workflows/pages.yml # build + deploy to GitHub Pages
```

## Building

Requires the `zola` binary. Common tasks are in the `Makefile`:

```sh
make serve    # local dev server with live reload
make build    # build into public/
make check    # validate without writing output
```

Regenerating publications after editing the `.bib` files (needs
[`uv`](https://docs.astral.sh/uv/)):

```sh
make env      # create the Python env (one-time)
make bib      # regenerate content/publications and content/patents
```

On Windows without GNU Make, run the underlying commands directly, e.g.:

```powershell
uv run scripts/import_bibtex.py data/papers.bib content/publications --overwrite
uv run scripts/import_bibtex.py data/patents.bib content/patents --overwrite
zola serve
```

## Deployment

Pushing to `main` triggers `.github/workflows/pages.yml`, which installs the
pinned Zola version, runs `zola build`, and publishes `public/` to the
`gh-pages` branch. `base_url` in `config.toml` must match the deployed URL.

## Customization notes

- **Profile photo:** `data/cv.yaml` points `profile.photo` at `img/portrait.jpg`
  (under `static/img/`). Zola generates AVIF, WebP, and JPEG variants at build
  time via `resize_image`. If the source is missing, the avatar falls back to
  initials automatically.
- **Bulma version:** change `extra.bulma_version` in `config.toml`.
- **Navigation:** edit `extra.menu` in `config.toml`.
- **Social icons:** SVG files live in `static/icons/`. Map each `name` from
  `data/cv.yaml` to a file in `[extra.social_icons]` in `config.toml`. Icons are
  rendered with a CSS mask so their color follows `--site-btn-social-color`. Use
  standard Font Awesome `svgs/` exports (not `svgs-full/` or `-square` variants).
  Unknown names fall back to `icons/link.svg`.

## Theming and colors

All site colors are defined in one place: the `:root` block at the top of
`static/css/custom.css`. The rest of that file references these variables only —
there are no other hard-coded hex colors in the stylesheet.

Templates do **not** choose colors. They use semantic class names for roles
(`cv-date`, `profile-role`, `pub-venue`, `tag-interest`, `btn-outlined`, and so
on) plus Bulma **layout** classes (`title`, `content`, `button`, `tag`, `card`).
All color values for those roles are assigned in `custom.css`.

### Bulma tokens (default text and links)

These control typography sitewide for Bulma layout classes (body text, headings,
inline links in prose):

| Variable | Role |
|----------|------|
| `--bulma-text-l` | Main body text lightness |
| `--bulma-text-strong-l` | Bold / emphasis text |
| `--bulma-text-title-l` | Heading text |
| `--bulma-text-weak-l` | Muted text (dates, footer, secondary lines) |
| `--bulma-link-h`, `--bulma-link-s`, `--bulma-link-l` | Link and accent blue |

### Semantic text classes

Muted/secondary text uses these template classes; color is set only in CSS:

| Class | Used for |
|-------|----------|
| `profile-role` | Job title on the About page |
| `cv-date` | Date ranges on CV cards |
| `cv-org` | Organization / institution lines |
| `cv-highlights` | Education highlight lists |
| `cv-summary` | Award summaries |
| `pub-authors` | Publication author lists |
| `pub-venue` | Journal / conference names |
| `footer-meta` | Footer timestamp |

### Tags and buttons

Tag and button **colors** are also defined in CSS via site tokens and role
classes (`tag-pub-type`, `tag-interest`, `btn-outlined`, `btn-doi`, etc.). Edit
the `--site-tag-*` and `--site-btn-*` variables in `:root` to restyle them.

### Site tokens (surfaces, borders, accents)

These control non-text styling defined in `custom.css`:

| Variable | Role |
|----------|------|
| `--site-bg` | Page background |
| `--site-surface` | Navbar, footer, search dropdown |
| `--site-surface-muted` | Publication detail meta box |
| `--site-surface-code` | BibTeX code block |
| `--site-surface-avatar` | Avatar placeholder background |
| `--site-border` | Standard borders |
| `--site-border-input` | Search input / dropdown border |
| `--site-border-subtle` | Light dividers (e.g. search results) |
| `--site-accent-education` | Education card left border |
| `--site-accent-award` | Awards card left border |
| `--site-highlight` | Search match highlight |
| `--site-shadow-*` | Navbar, card, and dropdown shadows |
| `--site-tag-*` | Tag background and text colors |
| `--site-btn-*` | Button background, border, and text colors |

To change the site's look, edit the `:root` block and the semantic class rules
in `custom.css`. Template changes are not required for color tweaks.

`static/processed_images/` (portrait AVIF/WebP/JPEG variants generated by Zola at
build time) is listed in `.gitignore` and should not be committed; the source
image is `static/img/portrait.jpg`.
