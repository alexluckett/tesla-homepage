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
  back to plain direct links with no bootstrap.

## Using it

**Country** — the dropdown sets which channels are offered and which regional URL each one
gets. Defaults to the UK. Each option is a flag followed by the country name; the flag is
there to scan by, the name to read. Flag emoji render on the Tesla's Android-based browser,
but some platforms (Windows Chrome among them) substitute the two-letter code instead —
which is why the name is spelled out rather than left to the flag alone.

**Edit** — tap it, or **long-press any card**, and every channel for that country appears,
including ones you have hidden (dimmed, dashed). Tap **Done** to go back. Both routes in
are kept: the button is always there, the long press saves reaching for it.

In edit mode a card does two things:

- **Tap** to show or hide it.
- **Drag** it to reorder. Order is stored per country, like hidden channels, and a channel
  added in a later release falls to the end rather than disappearing.

A gesture is read as a drag once the pointer moves more than 8px, so a slightly imprecise
tap still toggles rather than shuffling the grid.

Hidden channels are stored **per country**. Switching to another country shows that
market's full list from scratch; switching back restores the list you had filtered down.

## Storage

Three `localStorage` keys, each written only when you change something:

| Key | Contents |
| --- | --- |
| `frontrow.market` | The selected country code. |
| `frontrow.hidden` | `{"uk":["iplayer"],"us":[...]}` — hidden channels, per country. |
| `frontrow.order` | `{"uk":["netflix","plex",...]}` — channel order, per country. |

No cookies and no analytics. Every read and write is wrapped in `try`/`catch`, so the app
still runs where site data is blocked — it just forgets between sessions.

`?c=<code>` still works and wins for that visit (handy for a bookmark that always opens a
particular market); otherwise the stored choice is restored.

`fs` governs two separate behaviours — whether the launcher bootstraps itself into the
full-screen view, and whether each channel is routed through the redirect — so it takes
three settings:

| `fs` | Launcher bootstraps | Channels |
| --- | --- | --- |
| absent (default) | yes | direct links |
| `all` | yes | via the YouTube redirect |
| `0` or `off` | no | direct links |

The default costs **one interstitial per session, not one per channel**: the full-screen
view survives a same-window navigation, so once the launcher is in it, plain links stay
there too. This was confirmed on a car rather than assumed.

`fs=all` restores a redirect on every channel, for a firmware where that turns out not to
hold. `fs=once` is the old name for the default and still resolves to it, so bookmarks
written before the change keep working.

`fs` has no on-screen control by design — it is a property of the bookmark, not an
everyday setting.

`stay` is separate: it suppresses the bounce for one load and then deletes itself from the
address bar, so the launcher can be bookmarked at all. See below.

### Running the launcher itself full screen

The launcher bootstraps itself: on load the page bounces once through the YouTube redirect
back to itself, so tapping **Go to site** lands you in the full-screen view with Front Row
already in it. Nothing to hand-encode. Use `?stay` to save the bookmark in the first place
— see below.

The bounce is skipped when `fs=0` is set, so `?fs=0` remains a complete opt-out: no
bootstrap and no redirect on the channels either.

#### Bookmarking it on the car

The bounce lands the page inside the YouTube app's full-screen view, which has **no
bookmark control**. Since it fires the moment you arrive, there is otherwise no point at
which the launcher can be saved to favourites. `?stay` exists for this:

1. In the car's browser, open your deployment with `?stay` on the end:

   ```
   https://example.com/?stay
   ```

2. The page loads normally, in the ordinary browser. It does not jump to YouTube.
3. `stay` deletes itself from the address bar, which now reads
   `https://example.com/?c=uk`. That clean URL is what a bookmark captures.
4. Bookmark it.
5. Every launch from that bookmark goes full screen.

`?stay` works every time, so it is also the way back if a bookmark is lost or the address
changes.

**The first visit also never bounces**, which covers a fresh browser without needing
`?stay` — but it applies only once, so `?stay` is the reliable route. That rule is skipped
where storage is unavailable, since then every visit would look like the first and the
launcher would never bootstrap at all.

The bounce is also skipped when the page is running inside a frame, where navigating the
whole window out to YouTube is never what is wanted.

A refresh does not re-bounce, and nor does going back. Because `boot=1` is stripped from
the address bar on arrival, a reload would otherwise be indistinguishable from a cold open;
the page checks the Navigation Timing entry's `type` instead, so only a genuine navigation
bootstraps.

**Loop safety.** An unguarded version of this is an infinite redirect in a moving car, so
there are two independent guards and either alone is enough to stop it:

1. the `boot=1` parameter carried through the redirect and checked on return, and
2. a timestamp in `localStorage`, which suppresses a second attempt within 30 seconds
   even if that parameter is lost.

Both would have to fail simultaneously to get a cycle. This is verified: with the
parameter stripped entirely, six consecutive reloads produce exactly one bounce.

`boot=1` is removed from the address bar on arrival, so bookmarking the page as it sits
still bootstraps next time.

The bounce is script-initiated, which some engines refuse without a real user gesture. It
has been observed firing on a Tesla, so there is no manual fallback control; if a future
firmware stops honouring it the page simply stays windowed rather than breaking.

The browser's Fullscreen API is not a substitute: it fills the browser's viewport, and the
Tesla browser is itself a window in the car's UI, so it cannot escape that container the
way handing the navigation to the YouTube app does.

## Channels

46 channels across 10 markets. A channel is only listed where it is in that market's list
in the `MARKETS` table, so nothing appears in a country it does not serve.

| Market | Channels |
| --- | --- |
| 🇬🇧 United Kingdom | Plex, YouTube, Netflix, Prime Video, Apple TV, Disney+, BBC iPlayer, ITVX, Channel 4, Channel 5, NOW, Paramount+, Crunchyroll |
| 🇮🇪 Ireland | + RTÉ Player, Virgin Media Play |
| 🇺🇸 United States | + Hulu, HBO Max, Peacock, Tubi, Pluto TV |
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
| Prime Video | Yes — local storefront | `amazon.co.uk` / `.com` / `.de` `/gp/video/storefront`, else `primevideo.com` |
| Apple TV | Yes — path-scoped | `tv.apple.com/<cc>` |
| YouTube | Locale only | `youtube.com/?persist_gl=1&gl=<CC>` |
| Netflix, Disney+, Paramount+, Crunchyroll | No — account-scoped | Single global domain |
| National broadcasters | Inherently | Their own domain, listed once per market |

Only the UK, US and German Amazon sites serve a Prime Video storefront at that path. Every
other market opens `primevideo.com`, which is the site Amazon's
[Prime Video provider page](https://www.primevideo.com/help?nodeId=202064890) names for
Ireland, Australia, France, Spain, Italy and the Netherlands. Canada is listed there as
`amazon.ca`, but its storefront path returns 404, so it opens `primevideo.com` too.

Every URL was checked in September 2026 against the service's official website on
Wikidata (or Amazon's provider page), the organisation on its TLS certificate, and its
domain registration. Channels that have rebranded point at their current domain rather than
the old one that redirects, so that a lapsed old domain can never be picked up by someone
else: ITVX (`itv.com`), HBO Max (`hbomax.com`), 10 play (`10.com.au`), M6+ (`m6.fr`), Mitele
(`mediasetinfinity.es`) and Virgin Media Play (`play.virginmediatelevision.ie`).

## Logos

Every tile shows the service's name, one way or another. Where the artwork already spells
it out — Plex, Apple TV, ITVX, NOW, Tubi, ZDF — the mark stands alone. Where the mark is a
symbol, the tile pairs it with the name as a lockup, so nothing depends on recognising an
unlabelled glyph. Channels with no mark at all show just the name.

That list is judged by eye, not by metadata: HBO Max, for instance, ships an abstract glyph
rather than its logotype, so its tile is labelled despite the icon nominally being the
brand's mark.

Note that Simple Icons is an *icon* set, not a logotype set: its marks are monochrome
24x24 glyphs, so a proper brand lockup is assembled here rather than supplied. No open
pack covering these brands' logotypes was available — in particular the national
broadcasters, which developer-oriented logo collections do not carry. `LOGO_DIR` below is
the way to use real logotype artwork.

Marks are inlined as SVG paths so they cost no extra requests, and come from four sets:

| Set | Licence | Used for |
| --- | --- | --- |
| [Simple Icons](https://github.com/simple-icons/simple-icons) v16.30.0 | CC0-1.0 | most marks |
| [CoreUI Brands](https://github.com/coreui/coreui-icons) | CC0-1.0 | Hulu |
| [selfh.st/icons](https://github.com/selfhst/icons) | **CC BY 4.0** | Disney+, Prime Video |
| [Streamline Logos](https://www.streamlinehq.com/) | **CC BY 4.0** | BBC iPlayer |
| [custom-brand-icons](https://github.com/elax46/custom-brand-icons) | **CC BY-NC-SA 4.0** | Channel 5 |

The bottom three require attribution — that is what this table is for; keep it if you fork.

**The Channel 5 mark carries the strictest terms here**: CC BY-NC-SA 4.0 is
non-commercial, and its ShareAlike clause asks that derivatives be licensed alike. That is
fine for a private launcher, but if this repository is ever put to commercial use or
relicensed, delete `channel5`'s `p`/`t`/`vb` fields from the data blob — the tile falls
back to its name and nothing else breaks.

The sets draw on different grids and some marks sit in a corner of theirs, so each mark
carries its own `vb` (a viewBox tightened to the artwork's bounding box) where it is not
the 24x24 default. That is what keeps a 512x512 logotype and a 24x24 glyph the same
optical size on their tiles.

### A note on Simple Icons mirrors

Simple Icons no longer ships `primevideo`, `bbciplayer` or `amazon` — they are absent from
v16.30.0 on npm. Iconify's bundled copy is *labelled* v16.30.0 but still contains all
three, so it is a stale mirror from before those removals. Simple Icons runs a documented
removal process for brands that ask, so those marks are deliberately not taken from the
mirror; the Disney+, Prime Video and iPlayer artwork above comes from projects that drew
their own instead. The logos themselves remain the trademarks of their respective owners; Simple
Icons' [disclaimer](https://github.com/simple-icons/simple-icons/blob/develop/DISCLAIMER.md)
asks users to seek the permissions their project needs. Using them to label a link to the
service they belong to, in a private launcher, is ordinary identifying use.

**With a mark:** Plex, YouTube, Netflix, Prime Video, Apple TV, Disney+, BBC iPlayer, ITVX,
Channel 4, Channel 5, NOW, Paramount+, Crunchyroll, HBO Max, Tubi, Hulu, CBC Gem, ZDF, RTL+,
Virgin Media Play.

**Name only:** Peacock, Pluto TV, Crave, RTÉ Player, and the Australian, French, Spanish,
Italian, Dutch and German public broadcasters. `LOGO_DIR` below is the way to supply
these.

Brand colours are used exactly as the pack ships them, except where a mark would be
invisible on the dark background. Anything below 35% lightness is lifted in HSL so the hue
survives — blending toward white turns saturated reds into pink. That affects three:
**Apple TV** and **HBO Max** (both defined as black or dark grey, lifted to silver) and **NOW**
(a near-black teal, lifted to cyan). Hulu carries no colour in CoreUI Brands, so its tile
uses the brand's green. Disney+, Prime Video and BBC iPlayer are white logotypes: their
baked-in fill is stripped so they take the tile tint like every other mark.

### Using your own artwork instead

Point `LOGO_DIR` at a folder, near the top of the `<script>` block:

```js
var LOGO_DIR = "logos";
```

Each tile loads `<LOGO_DIR>/<channel id>.svg` and swaps it in once it decodes, replacing
the whole lockup (mark and label both) so your logotype is not doubled up with the built-in
name. Anything missing or broken keeps whatever the tile already had, so a partial set is
fine — this is the cleanest way to fill in the name-only channels above. `logos/README.md`
lists every channel id and the four with no mark at all. An `<img>` cannot be recoloured
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
