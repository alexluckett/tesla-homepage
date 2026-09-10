import json

icons = json.load(open('icons2.json'))

# name, icon slug (None = text wordmark fallback), and either a fixed url or a
# per-market map. A channel is only offered where it is listed in MARKETS below.
S = {
 'plex':        ('Plex',                'plex',          'https://app.plex.tv/desktop/'),
 'youtube':     ('YouTube',             'youtube',       None),
 'netflix':     ('Netflix',             'netflix',       'https://www.netflix.com/browse'),
 'prime':       ('Prime Video',          None,           None),
 'appletv':     ('Apple TV',            'appletv',       None),
 'disneyplus':  ('Disney+',              None,           'https://www.disneyplus.com/'),
 'paramountplus':('Paramount+',         'paramountplus', 'https://www.paramountplus.com/'),
 'crunchyroll': ('Crunchyroll',         'crunchyroll',   'https://www.crunchyroll.com/'),
 # UK
 'iplayer':     ('BBC iPlayer',          None,           'https://www.bbc.co.uk/iplayer'),
 'itvx':        ('ITVX',                'itvx',          'https://www.itvx.com/'),
 'channel4':    ('Channel 4',           'channel4',      'https://www.channel4.com/'),
 'channel5':    ('Channel 5',            None,           'https://www.channel5.com/'),
 'now':         ('NOW',                 'now',           'https://www.nowtv.com/'),
 # Ireland
 'rteplayer':   ('RTE Player',           None,           'https://www.rte.ie/player/'),
 'vmplayer':    ('Virgin Media Player', 'virginmedia',   'https://www.virginmediaplayer.ie/'),
 # United States
 'hulu':        ('Hulu',                 None,           'https://www.hulu.com/'),
 'max':         ('Max',                 'max',           'https://www.max.com/'),
 'peacock':     ('Peacock',              None,           'https://www.peacocktv.com/'),
 'tubi':        ('Tubi',                'tubi',          'https://tubitv.com/'),
 'pluto':       ('Pluto TV',             None,           'https://pluto.tv/'),
 # Canada
 'cbcgem':      ('CBC Gem',             'cbc',           'https://gem.cbc.ca/'),
 'crave':       ('Crave',                None,           'https://www.crave.ca/'),
 # Australia
 'abciview':    ('ABC iview',            None,           'https://iview.abc.net.au/'),
 'sbs':         ('SBS On Demand',        None,           'https://www.sbs.com.au/ondemand'),
 'ninenow':     ('9Now',                 None,           'https://www.9now.com.au/'),
 'sevenplus':   ('7plus',                None,           'https://7plus.com.au/'),
 'tenplay':     ('10 play',              None,           'https://10play.com.au/'),
 'stan':        ('Stan',                 None,           'https://www.stan.com.au/'),
 'binge':       ('Binge',                None,           'https://binge.com.au/'),
 # Germany
 'ard':         ('ARD Mediathek',        None,           'https://www.ardmediathek.de/'),
 'zdf':         ('ZDF',                 'zdf',           'https://www.zdf.de/'),
 'joyn':        ('Joyn',                 None,           'https://www.joyn.de/'),
 'rtlplus':     ('RTL+',                'rtl',           'https://plus.rtl.de/'),
 # France
 'francetv':    ('france.tv',            None,           'https://www.france.tv/'),
 'arte':        ('ARTE',                 None,           'https://www.arte.tv/fr/'),
 'tf1':         ('TF1+',                 None,           'https://www.tf1.fr/'),
 'm6':          ('M6+',                  None,           'https://www.6play.fr/'),
 'canalplus':   ('Canal+',               None,           'https://www.canalplus.com/'),
 # Spain
 'rtveplay':    ('RTVE Play',            None,           'https://www.rtve.es/play/'),
 'atresplayer': ('Atresplayer',          None,           'https://www.atresplayer.com/'),
 'mitele':      ('Mitele',               None,           'https://www.mitele.es/'),
 # Italy
 'raiplay':     ('RaiPlay',              None,           'https://www.raiplay.it/'),
 'infinity':    ('Mediaset Infinity',    None,           'https://mediasetinfinity.mediaset.it/'),
 'nowit':       ('NOW',                 'now',           'https://www.nowtv.it/'),
 # Netherlands
 'npo':         ('NPO Start',            None,           'https://npo.nl/start'),
 'videoland':   ('Videoland',            None,           'https://www.videoland.com/'),
}

AMAZON = {'uk':'www.amazon.co.uk','ie':None,'us':'www.amazon.com','ca':'www.amazon.ca',
          'au':'www.amazon.com.au','de':'www.amazon.de','fr':'www.amazon.fr',
          'es':'www.amazon.es','it':'www.amazon.it','nl':'www.amazon.nl'}
APPLE = {'uk':'gb','ie':'ie','us':'us','ca':'ca','au':'au','de':'de','fr':'fr',
         'es':'es','it':'it','nl':'nl'}
YT = {k:(v.upper() if k!='uk' else 'GB') for k,v in APPLE.items()}

GLOBAL = ['plex','youtube','netflix','prime','appletv','disneyplus']
MARKETS = [
 ('uk','\U0001F1EC\U0001F1E7','United Kingdom', GLOBAL+['iplayer','itvx','channel4','channel5','now','paramountplus','crunchyroll']),
 ('ie','\U0001F1EE\U0001F1EA','Ireland',        GLOBAL+['rteplayer','vmplayer','paramountplus','crunchyroll']),
 ('us','\U0001F1FA\U0001F1F8','United States',  GLOBAL+['hulu','max','peacock','paramountplus','tubi','pluto','crunchyroll']),
 ('ca','\U0001F1E8\U0001F1E6','Canada',         GLOBAL+['cbcgem','crave','paramountplus','tubi','crunchyroll']),
 ('au','\U0001F1E6\U0001F1FA','Australia',      GLOBAL+['abciview','sbs','ninenow','sevenplus','tenplay','stan','binge','paramountplus','crunchyroll']),
 ('de','\U0001F1E9\U0001F1EA','Germany',        GLOBAL+['ard','zdf','joyn','rtlplus','paramountplus','crunchyroll']),
 ('fr','\U0001F1EB\U0001F1F7','France',         GLOBAL+['francetv','arte','tf1','m6','canalplus','crunchyroll']),
 ('es','\U0001F1EA\U0001F1F8','Spain',          GLOBAL+['rtveplay','atresplayer','mitele','crunchyroll']),
 ('it','\U0001F1EE\U0001F1F9','Italy',          GLOBAL+['raiplay','infinity','nowit','paramountplus','crunchyroll']),
 ('nl','\U0001F1F3\U0001F1F1','Netherlands',    GLOBAL+['npo','videoland','crunchyroll']),
]

# Icons whose artwork already spells the service name. Everything else is a
# symbol, and its tile pairs the mark with the name so no channel depends on
# recognising an unlabelled glyph.
SELF_NAMING = {'plex','appletv','itvx','now','nowit','max','tubi','zdf'}

services = {}
for sid,(name,slug,url) in S.items():
    e = {'n': name}
    if slug:
        e['p'] = icons[slug]['path']
        e['t'] = icons[slug]['tint']
        if sid in SELF_NAMING:
            e['w'] = 1
    if sid == 'youtube':
        e['u'] = {m: 'https://www.youtube.com/?persist_gl=1&gl=' + YT[m] for m,_,_,_ in MARKETS}
        e['native'] = True
    elif sid == 'prime':
        e['u'] = {m: ('https://%s/gp/video/storefront' % AMAZON[m]) if AMAZON[m]
                     else 'https://www.primevideo.com/' for m,_,_,_ in MARKETS}
    elif sid == 'appletv':
        e['u'] = {m: 'https://tv.apple.com/' + APPLE[m] for m,_,_,_ in MARKETS}
    else:
        e['u'] = url
    services[sid] = e

markets = [{'c':c,'f':f,'n':n,'ch':ch} for c,f,n,ch in MARKETS]

for m in markets:
    for sid in m['ch']:
        assert sid in services, (m['c'], sid)

blob = json.dumps({'s': services, 'm': markets}, ensure_ascii=False, separators=(',',':'))
open('data.json','w').write(blob)
print('services:', len(services), '| markets:', len(markets), '| blob:', len(blob), 'bytes')
print('per market:', ', '.join('%s=%d' % (m['c'], len(m['ch'])) for m in markets))
print('text-only:', ', '.join(sorted(k for k,v in services.items() if 'p' not in v)))
