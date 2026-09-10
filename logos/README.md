# Drop logo files here

Any SVG placed here replaces that channel's built-in mark. Name each file after the
channel id, then turn the folder on with one line near the top of the `<script>` block in
`../index.html`:

```js
var LOGO_DIR = "logos";
```

It is off by default so the page makes no image requests at all. With it on, every channel
in the current market requests its file, and any that 404 simply keep the built-in mark —
so a partial set is fine.

## The four with no mark at all

These currently render as a plain name, because no CC0 icon set carries them (Simple
Icons, CoreUI Brands and gilbarbara/logos were all checked):

```
prime.svg        Prime Video
disneyplus.svg   Disney+
iplayer.svg      BBC iPlayer
channel5.svg     Channel 5
```

## Every channel id

```
plex  youtube  netflix  prime  appletv  disneyplus  paramountplus  crunchyroll
iplayer  itvx  channel4  channel5  now                                    (UK)
rteplayer  vmplayer                                                       (IE)
hulu  max  peacock  tubi  pluto                                           (US)
cbcgem  crave                                                             (CA)
abciview  sbs  ninenow  sevenplus  tenplay  stan  binge                   (AU)
ard  zdf  joyn  rtlplus                                                   (DE)
francetv  arte  tf1  m6  canalplus                                        (FR)
rtveplay  atresplayer  mitele                                             (ES)
raiplay  infinity  nowit                                                  (IT)
npo  videoland                                                            (NL)
```

## Making them look right

- **Use light-on-dark variants.** Tiles are near-black; a dark logotype disappears. An
  `<img>` cannot be recoloured by CSS, so the colour has to be baked into the file.
- **Horizontal logotypes work best** — the tile is 3:2 landscape and caps the image at 70%
  width. A logo that includes the service name is ideal, since the built-in label is
  hidden once your file loads.
- **Keep them local.** Hotlinking a CDN means a third-party request from the car on every
  page load, which is the one thing this app otherwise never does.
- Most services publish brand or press-kit assets with usable SVGs.
