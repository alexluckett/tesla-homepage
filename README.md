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

## Adding a region or a service

Both live in the `<script>` block at the bottom of `index.html`:

- `COUNTRIES` — add a row with `code`, `label`, `name`, `apple`, `yt`, `amazon`. The
  picker is built from this table, so the buttons follow automatically.
- `SERVICES` — add an entry with `url(country)` and `host(country)`, then add a matching
  `<a class="tile" data-service="...">` to the deck. Set `native: true` for anything that
  should skip the YouTube bounce.

The deck grid is 3 columns with Plex spanning 2, which fills exactly at 3, 2 and 1
columns. If you add a sixth service, drop the `tile--wide` class from Plex so the grid
still fills.

## Design

Dark-only by intent — this runs on a car screen, often at night, where a light theme is a
headlight in the face. The interface chrome is warm monochrome and the only colour on the
page comes from the five service tints, so the tiles read at a glance while driving up to
a charger.
