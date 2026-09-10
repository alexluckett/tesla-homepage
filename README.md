# Front Row

A single-file streaming launcher for the Tesla browser. Big touch targets, region-aware
links, and every button routed through the YouTube redirect so the destination opens
full screen.

One file, no build step, no dependencies, no cookies, no storage, no analytics, and no
third-party requests (system fonts only). Drop `index.html` on any static host.

## How the full-screen trick works

The Tesla browser is a windowed webview, but the built-in **YouTube app** draws over the
whole screen. Navigating to:

```
https://www.youtube.com/redirect?q=<url-encoded destination>
```

hands the navigation to that app, which shows YouTube's "you are leaving YouTube"
interstitial. Tapping **Go to site** loads the destination *inside the full-screen view*.

Practical notes:

- Open the YouTube app once and close it first, so it is warm in memory.
- Video playback only works in **Park**.
- YouTube itself is linked directly — it is already the full-screen app, so wrapping it
  in its own redirect would only add a pointless interstitial.
- This is a firmware-dependent trick. Tesla has closed earlier full-screen holes before,
  and some owners have reported this one failing on particular builds. Use `?fs=0` to
  fall back to plain direct links.

## URL parameters

The page is stateless — everything lives in the query string, nothing is written to the
device.

| Parameter | Values | Default | Effect |
| --- | --- | --- | --- |
| `c` (or `country`) | `uk` `ie` `us` `ca` `au` `de` `fr` `es` `it` `nl` | `uk` | Region for the service links. `gb` is accepted as an alias for `uk`. |
| `fs` | `0` / `off` to disable | on | Turns the YouTube full-screen redirect off, giving direct links. |

Examples:

```
/index.html            → UK, full screen
/index.html?c=de       → Germany, full screen
/index.html?c=us&fs=0  → US, direct links
```

Both controls are also on the page; changing them rewrites the query string with
`history.replaceState`, so bookmarking the page keeps your choice.

The **Open Front Row full screen** link at the bottom is the page's own URL wrapped in
the YouTube redirect — bookmark that one so the launcher itself opens full screen.

## What region actually changes

Only the services that genuinely have per-country URLs:

| Service | Region-aware? | Target |
| --- | --- | --- |
| Plex | No — account-scoped | `app.plex.tv/desktop/` |
| YouTube | Locale only | `youtube.com/?persist_gl=1&gl=<CC>` |
| Apple TV | Yes — path-scoped | `tv.apple.com/<cc>` |
| Prime Video | Yes — local storefront | `<local amazon domain>/gp/video/storefront` |
| Netflix | No — account-scoped | `netflix.com/browse` |

Each tile prints its resolved host, so you can see exactly where a button goes before
you tap it.

## Logos

Four of the five channel marks are real brand icons, inlined as SVG paths straight into
`index.html` — nothing to download, no image requests, and they inherit each tile's
`--tint` so they sit properly on the dark ground.

They come from **[Simple Icons](https://github.com/simple-icons/simple-icons)** v16.30.0,
whose repository is released under **CC0-1.0**. The logos themselves remain the trademarks
of their respective owners; Simple Icons' own
[disclaimer](https://github.com/simple-icons/simple-icons/blob/develop/DISCLAIMER.md)
asks users to seek the permissions their project needs. Using them to label a link to the
service they belong to, in a private launcher, is ordinary identifying use.

Two adjustments to what the pack ships:

- **Apple TV** is defined as pure black, which is invisible on this background, so the
  tile tints it silver instead.
- **Prime Video is not in the pack** — there is no `primevideo` or `amazon` slug in
  v16.30.0. Simple Icons runs a documented removal process for brands that ask, and
  Amazon's absence from a pack this large is conspicuous, but I could not confirm that is
  the reason. That tile currently uses a generic play glyph. Drop a real asset in via
  `LOGO_DIR` below if you want one.

### Using your own artwork instead

Point `LOGO_DIR` at a folder, near the top of the `<script>` block:

```js
var LOGO_DIR = "logos";
```

```
logos/plex.svg   logos/youtube.svg   logos/appletv.svg
logos/prime.svg  logos/netflix.svg
```

Each tile loads `<LOGO_DIR>/<service id>.svg` and swaps it in once it decodes; anything
missing or broken falls back to the built-in glyph, so a partial set is fine — dropping in
`prime.svg` alone works. Note that an `<img>` cannot be recoloured by CSS, so bake the
colour into the file and use light-on-dark variants. Keep them local rather than
hotlinking a CDN: a remote logo is a third-party request from your car on every load.

## Adding a region or a service

Both live in the `<script>` block at the bottom of `index.html`:

- `COUNTRIES` — add a row with `code`, `label`, `name`, `apple`, `yt`, `amazon`. The
  picker is built from this table, so the buttons follow automatically.
- `SERVICES` — add an entry with `url(country)` and `host(country)`, then add a matching
  `<a class="tile" data-service="...">` to the deck. Set `native: true` for anything that
  should skip the YouTube bounce.

The deck is a single row of five equal tiles on any screen wide enough to hold them —
which is every car screen — and one equal column below 860px. Both layouts fill exactly,
so no tile is left stranded on a row of its own. If you change the number of services,
update `grid-template-columns: repeat(5, 1fr)` in `.deck` to match, and give the new tile
a `.glyph` SVG and a `--tint` colour.

## Design

Equal-sized channel tiles in one rack, the way a TV platform lists its apps: a brand glyph
over a uniform, quiet name label, so the logo does the identifying and the type does not
compete with it. Dark-only by intent — this runs on a car screen, often at night, where a light theme is a
headlight in the face. The interface chrome is warm monochrome and the only colour on the
page comes from the five service tints, so the tiles read at a glance while driving up to
a charger.
