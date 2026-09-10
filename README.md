# Front Row

A streaming launcher for the Tesla browser. Pick a country, tap a channel — every button
routed through the YouTube redirect so the destination opens full screen.

One file, no build step, no dependencies, no analytics, and no third-party requests
(system fonts, inlined SVG). Drop `index.html` on any static host.

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

## Using it

**Country** — the dropdown sets which channels are offered and which regional URL each one
gets. Defaults to the UK. It shows flags only; the country name is on each option's
tooltip. Flag emoji render on the Tesla's Android-based browser, but some platforms
(Windows Chrome among them) substitute the two-letter code instead — still legible, just
less pretty.

**Edit** — tap it and every channel for that country appears, including ones you have
hidden (dimmed, dashed). Tap any tile to toggle it. Tap **Done** to go back. There is no
long-press or drag: both are unpleasant to hit accurately in a moving car.

Hidden channels are stored **per country**. Switching to another country shows that
market's full list from scratch; switching back restores the list you had filtered down.

## Storage

Two `localStorage` keys, both written only when you change something:

| Key | Contents |
| --- | --- |
| `frontrow.market` | The selected country code. |
| `frontrow.hidden` | `{"uk":["iplayer"],"us":[...]}` — hidden channels, per country. |

No cookies and no analytics. Every read and write is wrapped in `try`/`catch`, so the app
still runs where site data is blocked — it just forgets between sessions.

`?c=<code>` still works and wins for that visit (handy for a bookmark that always opens a
particular market); otherwise the stored choice is restored. `?fs=0` disables the
full-screen redirect and has no on-screen control by design — it is an escape hatch for
firmware that has closed the trick, not an everyday setting.

## Channels

46 channels across 10 markets. A channel is only listed where it is in that market's list
in the `MARKETS` table, so nothing appears in a country it does not serve.

| Market | Channels |
| --- | --- |
| 🇬🇧 United Kingdom | Plex, YouTube, Netflix, Prime Video, Apple TV, Disney+, BBC iPlayer, ITVX, Channel 4, Channel 5, NOW, Paramount+, Crunchyroll |
| 🇮🇪 Ireland | + RTÉ Player, Virgin Media Player |
| 🇺🇸 United States | + Hulu, Max, Peacock, Tubi, Pluto TV |
| 🇨🇦 Canada | + CBC Gem, Crave, Tubi |
| 🇦🇺 Australia | + ABC iview, SBS On Demand, 9Now, 7plus, 10 play, Stan, Binge |
| 🇩🇪 Germany | + ARD Mediathek, ZDF, Joyn, RTL+ |
| 🇫🇷 France | + france.tv, ARTE, TF1+, M6+, Canal+ |
| 🇪🇸 Spain | + RTVE Play, Atresplayer, Mitele |
| 🇮🇹 Italy | + RaiPlay, Mediaset Infinity, NOW |
| 🇳🇱 Netherlands | + NPO Start, Videoland |

("+" is in addition to the six global channels: Plex, YouTube, Netflix, Prime Video,
Apple TV, Disney+.)

### Which URLs are regional

Only where the service genuinely differs by market:

| Channel | Regional? | Target |
| --- | --- | --- |
| Prime Video | Yes — local storefront | `amazon.co.uk` / `.de` / `.com.au` … `/gp/video/storefront` |
| Apple TV | Yes — path-scoped | `tv.apple.com/<cc>` |
| YouTube | Locale only | `youtube.com/?persist_gl=1&gl=<CC>` |
| Netflix, Disney+, Paramount+, Crunchyroll | No — account-scoped | Single global domain |
| National broadcasters | Inherently | Their own domain, listed once per market |

Ireland is the exception on Prime Video: it uses `primevideo.com` rather than an Amazon
storefront domain.

> **Unverified.** The build environment had no outbound network access, so none of these
> URLs could be checked live. Most are long-stable domains, but a few have had recent
> rebrands and are worth confirming before you rely on them: **TF1+** (`tf1.fr`),
> **M6+** (`6play.fr`), **NPO Start** (`npo.nl/start`), **Mitele** (`mitele.es`) and
> **Mediaset Infinity**.

## Logos

Every tile shows the service's name, one way or another. Where the artwork already spells
it out — Plex, Apple TV, ITVX, NOW, Tubi, ZDF — the mark stands alone. Where the mark is a
symbol, the tile pairs it with the name as a lockup, so nothing depends on recognising an
unlabelled glyph. Channels with no mark at all show just the name.

That list is judged by eye, not by metadata: Max, for instance, ships an abstract glyph
rather than its logotype, so its tile is labelled despite the icon nominally being the
brand's mark.

Note that Simple Icons is an *icon* set, not a logotype set: its marks are monochrome
24x24 glyphs, so a proper brand lockup is assembled here rather than supplied. No open
pack covering these brands' logotypes was available — in particular the national
broadcasters, which developer-oriented logo collections do not carry. `LOGO_DIR` below is
the way to use real logotype artwork.

Marks come from two **CC0-1.0** sets, inlined as SVG paths so they cost no extra requests:
**[Simple Icons](https://github.com/simple-icons/simple-icons)** v16.30.0 for most of them,
and **[CoreUI Brands](https://github.com/coreui/coreui-icons)** for Hulu. The two use
different grids, so each mark carries its own `vb` (viewBox) where it is not the 24x24
default. The logos themselves remain the trademarks of their respective owners; Simple
Icons' [disclaimer](https://github.com/simple-icons/simple-icons/blob/develop/DISCLAIMER.md)
asks users to seek the permissions their project needs. Using them to label a link to the
service they belong to, in a private launcher, is ordinary identifying use.

**With a mark:** Plex, YouTube, Netflix, Apple TV, ITVX, Channel 4, NOW, Paramount+,
Crunchyroll, Max, Tubi, Hulu, CBC Gem, ZDF, RTL+, Virgin Media Player.

**Name only** (in none of the sets searched): Prime Video, Disney+, BBC iPlayer, Channel 5,
Peacock, Pluto TV, Crave, RTÉ Player, and the Australian, French, Spanish, Italian, Dutch
and German public broadcasters. Simple Icons, CoreUI Brands and the gilbarbara `logos` set
were all checked — roughly 3,000 icons — and broadcaster logotypes are simply not what
developer icon sets carry. `LOGO_DIR` below is the way to supply them.

Brand colours are used exactly as the pack ships them, except where a mark would be
invisible on the dark background. Anything below 35% lightness is lifted in HSL so the hue
survives — blending toward white turns saturated reds into pink. That affects three:
**Apple TV** and **Max** (both defined as black or dark grey, lifted to silver) and **NOW**
(a near-black teal, lifted to cyan). Hulu carries no colour in CoreUI Brands, so its tile
uses the brand's green.

### Using your own artwork instead

Point `LOGO_DIR` at a folder, near the top of the `<script>` block:

```js
var LOGO_DIR = "logos";
```

Each tile loads `<LOGO_DIR>/<channel id>.svg` and swaps it in once it decodes; anything
missing or broken keeps whatever the tile already had, so a partial set is fine — this is
the cleanest way to fill in the name-only channels above. An `<img>` cannot be recoloured
by CSS, so bake the colour into the file and use light-on-dark variants. Keep them local
rather than hotlinking a CDN: a remote logo is a third-party request from your car on every
load.

## Adding a channel or a market

Both tables are generated into the `<script id="data">` blob by
`build_data.py` (see the repository history) but can be edited in place in `index.html`:

- A channel is `{"n": "Name", "p": "<svg path>", "t": "#tint", "u": "<url>"}`. `u` may
  instead be an object keyed by market code for a regional URL. Omit `p`/`t` to get the
  name-only tile. Add `"native": true` for anything that should skip the YouTube bounce.
- A market is `{"c": "uk", "f": "🇬🇧", "n": "United Kingdom", "ch": [channel ids]}`. The
  dropdown is built from this list, so a new market appears automatically.

The grid is `repeat(auto-fill, minmax(180px, 1fr))`, so it absorbs any number of channels
without further changes. The control bar and the grid share one measure, `--shell`
(1080px), and both centre on wider screens — change it in one place to widen or narrow the
whole layout.

## Design

The screen is the channels. No on-page explanation, no status text, no settings panel —
a launcher that needs instructions on the glass has failed. The only chrome is a quiet
wordmark, the country dropdown and the Edit button.

Dark-only by intent — this runs on a car screen, often at night, where a light theme is a
headlight in the face. The interface is warm monochrome and the only colour comes from the
channel marks themselves.
