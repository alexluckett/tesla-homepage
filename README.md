# Front Row

A streaming launcher for the Tesla browser. Five channels, a region dropdown, nothing
else — every button routed through the YouTube redirect so the destination opens full
screen.

One file, no build step, no dependencies, no cookies, no storage, no analytics, and no
third-party requests (system fonts, inlined SVG). Drop `index.html` on any static host.

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
  and some owners have reported this one failing on particular builds. Add `?fs=0` to fall
  back to plain direct links.

## URL parameters

The page is stateless — everything lives in the query string, nothing is written to the
device.

| Parameter | Values | Default | Effect |
| --- | --- | --- | --- |
| `c` (or `country`) | `uk` `ie` `us` `ca` `au` `de` `fr` `es` `it` `nl` | `uk` | Region for the channel links. `gb` is accepted as an alias for `uk`. |
| `fs` | `0` / `off` to disable | on | Turns the YouTube full-screen redirect off, giving direct links. |

Picking a region from the dropdown rewrites `c` with `history.replaceState`, so
bookmarking the page keeps your choice. `fs` has no on-screen control by design — it is
an escape hatch for a firmware that has closed the trick, not an everyday setting.

### Bookmarking it full screen

So the launcher *itself* opens full screen, bookmark the page wrapped in the same
redirect — URL-encode your deployed address as the `q` value:

```
https://www.youtube.com/redirect?q=https%3A%2F%2Fexample.com%2F%3Fc%3Duk
```

## What region actually changes

Only the channels that genuinely have per-country URLs:

| Channel | Region-aware? | Target |
| --- | --- | --- |
| Plex | No — account-scoped | `app.plex.tv/desktop/` |
| YouTube | Locale only | `youtube.com/?persist_gl=1&gl=<CC>` |
| Apple TV | Yes — path-scoped | `tv.apple.com/<cc>` |
| Prime Video | Yes — local storefront | `<local amazon domain>/gp/video/storefront` |
| Netflix | No — account-scoped | `netflix.com/browse` |

## Logos

Four of the five marks are real brand icons, inlined as SVG paths in `index.html` —
nothing to download, and they inherit each tile's `--tint` so they sit properly on the
dark ground.

They come from **[Simple Icons](https://github.com/simple-icons/simple-icons)** v16.30.0,
whose repository is released under **CC0-1.0**. The logos themselves remain the trademarks
of their respective owners; Simple Icons'
[disclaimer](https://github.com/simple-icons/simple-icons/blob/develop/DISCLAIMER.md) asks
users to seek the permissions their project needs. Using them to label a link to the
service they belong to, in a private launcher, is ordinary identifying use.

Two adjustments to what the pack ships:

- **Apple TV** is defined as pure black, invisible on this background, so the tile tints
  it silver.
- **Prime Video is not in the pack** — there is no `primevideo` or `amazon` slug in
  v16.30.0. Simple Icons runs a documented removal process for brands that ask, and
  Amazon's absence from a pack this large is conspicuous, but I could not confirm that is
  the reason. That tile uses a generic play glyph.

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
missing or broken keeps the built-in glyph, so a partial set is fine — dropping in
`prime.svg` alone works. An `<img>` cannot be recoloured by CSS, so bake the colour into
the file and use light-on-dark variants. Keep them local rather than hotlinking a CDN: a
remote logo is a third-party request from your car on every load.

## Adding a region or a channel

Both live in the `<script>` block at the bottom of `index.html`:

- `COUNTRIES` — add a row with `code`, `name`, `apple`, `yt`, `amazon`. The dropdown is
  built from this table, so the option appears automatically.
- `SERVICES` — add an entry with `url(country)`, then add a matching
  `<a class="tile" data-service="...">` to the deck with its own `.glyph` SVG and `--tint`
  colour. Set `native: true` for anything that should skip the YouTube bounce.

The deck is one row of five equal tiles on any screen wide enough — every car screen — and
equal full-width rows below 880px. If you change the number of channels, update
`grid-template-columns: repeat(5, 1fr)` in `.deck` to match.

## Design

The screen is the channels. There is no on-page explanation, no status text and no
settings panel: a launcher that needs instructions on the glass has failed. The only
chrome is a whisper-quiet wordmark and the region dropdown.

Dark-only by intent — this runs on a car screen, often at night, where a light theme is a
headlight in the face. The interface is warm monochrome and the only colour comes from the
five channel marks.
