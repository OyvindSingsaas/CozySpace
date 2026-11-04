# CozySpace

**Live: <https://oyvindsingsaas.github.io/CozySpace/>**

A living desktop background: Earth at the centre, and everything humanity is talking to in space,
on a log light-time scale out to the edge of the observable universe. Real data, fetched live by
the browser. Flat-vector, quiet, meant to sit behind your windows (e.g. via [Plash](https://sindresorhus.com/plash) on macOS).

## What you're looking at

Right now, a handful of large dishes in California, Spain and Australia are listening to spacecraft
scattered across the solar system: rovers on Mars, telescopes a million and a half kilometres out,
the two Voyagers, close to a light-day away. That's NASA's Deep Space Network, and it publishes
what every dish is doing, minute by minute. CozySpace draws those conversations as they happen.

**Earth sits in the middle**, as it is this moment: day and night where they really are, city lights
on the dark side, the aurora over both poles, the ISS passing over. The view is fixed relative to the
Sun, which always sits to the right, so you watch Earth turn underneath you through the day.

**Everything else is placed in its true direction**, as seen from Earth, and at a distance measured in
**light-time**: how long a signal takes to get there. The scale is logarithmic, so the Moon (1.3 light-seconds),
the Sun (8 light-minutes), Saturn (about an hour) and Voyager 1 (almost a full light-day) all fit on one
screen. Beyond the edge of the Sun's wind, the scale keeps going: the nearest stars (years), the galactic
centre (26 000 years), Andromeda (2.5 million) and, at the rim, the oldest light there is, the cosmic
microwave background (13.8 billion).

**The small travelling waves are the actual data.** Each one is a megabyte coming home (amber) or a
command going out (blue). They move at the speed of light, so the ones from Voyager have been on their
way for most of a day, and the ones from the Moon arrive almost at once (near Earth they are slowed down
a little so you can see them). When a dish starts or stops talking to a spacecraft, a ripple goes out.

**The rest of the live world shows up as events:** the Sun flares when the GOES satellites see X-rays
rise, sunspots drift across its face, and a small rocket climbs from the launch site whenever a real
launch happens somewhere on Earth.

**And a reminder of how far we've reached:** a faint ring marks how far our very first radio signals
(Marconi, 1901) have travelled since, about 125 light-years. Hover the Voyagers to hear the Golden Record
they carry, or the ring to watch the Arecibo message being written out.

Mostly, though, it's meant to be glanced at: a quiet sense that, right now, someone on Earth is listening
to something very far away.

## Running it

Opened straight from disk, browsers block the page from reading its own data files (sounds, ephemeris,
images). Serve the repo folder instead:

```
cd ~/"Documents/Private/Kode prosjekt/CozySpace" && python3 -m http.server 8000
```

then open <http://localhost:8000/sketch/>. Sound is on by default: it starts as soon as the browser allows (usually your first click or key press). The speaker button (top right) turns it off, and that choice is remembered.

URL options: `?fps=` (default 24), `?speed=`, `?offset=` (minutes), `?vmax=` (packet speed cap, px/s),
`?mb=` (MB per packet). Demos: `?ripples`, `?flare=M2.4`, `?launch`, `?nova`.

## Data

### Fetched live by the page

| Shown as | Source | Refreshed |
|---|---|---|
| Links between dishes and spacecraft, data rates, dish pointing | [NASA DSN Now](https://eyes.nasa.gov/dsn/dsn.html) `dsn.xml` (+ `config.xml` once, for names) | 30 s |
| Aurora ovals (north and south) | NOAA SWPC OVATION aurora nowcast | 30 min |
| Solar flares | NOAA GOES X-ray flux, last 6 h | 2 min |
| Sunspots on the Sun's disc | NOAA SWPC solar regions | 6 h |
| International Space Station | CelesTrak orbital elements, propagated in the browser with satellite.js | elements 12 h, position every frame |
| Rocket launches | Launch Library 2 (The Space Devs) | 30 min |
| Coastlines | world-atlas land map (jsDelivr) | once |

Polling pauses while the page is hidden. If a feed fails, that layer goes quiet and the rest carries on.

### Computed in the browser

Day and night, the Sun's direction and Earth's rotation, city lights on the night side, the Moon's
orbit, orbiters' and rovers' motion (real periods), the radio-bubble radius (light-years since 1901),
light-travel times, and all generated sound.

### Local files

| File | What | How it's made |
|---|---|---|
| `data/ephemeris.js` | Directions and distances of planets and spacecraft, a year at 2-day steps, interpolated to now | `python3 scripts/fetch_ephemeris.py` (JPL Horizons). Re-run every few months |
| `data/stories.js` | The short spacecraft stories for the hover box | Written by hand |
| `data/sounds.js` | The audio clips, packed into a script | `python3 scripts/pack_sounds.py` (needs ffmpeg) |
| `images/golden-record-engraving.png` | Golden Record cover, engraved lines only | Extracted from NASA's photo, `images/voyager-golden-record-cover.webp` |
| `data/dsn_log.csv` | A day of DSN polling, for studying pacing (not used by the page) | `python3 scripts/log_dsn.py` |

### Fixed

Deep-space objects (positions and distances), the Arecibo message bitmap (1679 bits), the heliopause
and Oort cloud distances.

## What happens on screen

| Event / element | Driven by |
|---|---|
| Wave packets travelling along each link: amber down (spacecraft to Earth), blue up | DSN data rate: 1 packet = 1 MB; uplinks one every 5 min. Real light speed, capped at 120 px/s on screen |
| Faint carrier pulses on every live link, every 15 s, so slow links still hum | Link is live |
| Dishes appearing, slewing and turning away | DSN dish assignments and az/el; real slew rates |
| Ripples at dish and spacecraft when a link starts (warm) or ends (cool) | DSN; a link that drops out of the feed for under 2½ min counts as continuous |
| The Sun flaring: sparks and loops sized by class (B, C, M, X) | GOES X-ray flux |
| Sunspots | NOAA active regions |
| Aurora breathing around both poles | OVATION nowcast |
| ISS crossing the globe | TLE + SGP4 |
| A small rocket climbing (shown at 5x altitude) for about 9 min, then a pulse at orbit | Launch Library 2 |
| Day/night line, city lights | Clock |
| Radio bubble: the ring our earliest radio has reached | Years since 12 Dec 1901 |
| Golden Record engraving tracing itself beside a Voyager | Hovering Voyager 1 or 2 |
| Arecibo message building in space, bit by bit (10 bit/s) | Hovering the radio ring |

Natural objects show only their light-time; hover for the name. Spacecraft are always named.

Hover a spacecraft, the ISS or a rising rocket and a small box in the lower right tells its story: when and how it
launched, who flies it, what it's for, a fact or two, and what it's doing right now (light-time, which dish is listening).
The stories live in `data/stories.js` (easy to edit); rockets take theirs from Launch Library. The **i** button turns the box off.

## Transmitting and receiving

### On Earth: NASA's Deep Space Network

| Complex | Location | Antennas seen in the feed |
|---|---|---|
| Goldstone | California, USA | DSS-14 (70 m), DSS-23, DSS-24, DSS-25, DSS-26 (34 m) |
| Madrid | Robledo de Chavela, Spain | DSS-63 (70 m), DSS-53, DSS-54, DSS-55, DSS-56, DSS-65 (34 m) |
| Canberra | Tidbinbilla, Australia | DSS-43 (70 m), DSS-34, DSS-35, DSS-36 (34 m) |

Only dishes currently assigned to a spacecraft are drawn; the 70 m dish sits in the middle of each cluster.
A complex on the far side of the globe sends its links from the horizon.

### In space

Any spacecraft the DSN talks to appears while it's being contacted. Placement:

| Where | Spacecraft (DSN code) |
|---|---|
| Near Earth | MMS (MMS1-4), Chandra, TESS, XMM-Newton, IBEX, TDRS, ESCAPADE Gold & Blue (ESCG, ESCB) |
| Moon | LRO, Danuri (KPLO), CAPSTONE, THEMIS-B/C (ARTEMIS), Chandrayaan-2, SLIM, Blue Ghost, IM-2, Orion / Artemis II |
| Sun–Earth L1 | SOHO, ACE, Wind, DSCOVR, IMAP, Aditya-L1, SWFO-L1, Carruthers |
| Sun–Earth L2 | JWST, Euclid, Gaia, SPHEREx, PLATO, Roman (RST) |
| Mars | MRO, MAVEN, Perseverance (M20), Curiosity (MSL), Mars Odyssey (M01O), TGO, Mars Express, Hope |
| Jupiter | Juno |
| Around the Sun | Parker Solar Probe, STEREO-A, Solar Orbiter, BepiColombo, Psyche, Lucy, Europa Clipper, JUICE |
| Outer solar system and beyond | New Horizons, Voyager 2, Voyager 1 |

Real positions (JPL Horizons) where `data/ephemeris.js` has them; otherwise an approximate place by its home. A code the page doesn't know (not in either) is skipped.
LRO, Danuri and Curiosity are always shown, orbiting or turning with their body, even when quiet.

Contacted on 3 Nov 2026 (from `data/dsn_log.csv`): Mars Odyssey, Voyager 2, ESCAPADE, Wind, New Horizons,
Parker, MRO, ACE, Danuri, SOHO, Roman, Voyager 1, LRO, THEMIS-C, STEREO-A, JWST, MMS.

Also shown, not on the DSN: the ISS, rockets on their way up, and the planets, Moon and Sun (light-time only).

## Sound

On by default, starting at the first click or key press (browsers block sound before that); the speaker button turns it off, remembered. One sound at a time; moving away stops it.

| Object | Sound | File | Credit |
|---|---|---|---|
| Background | Slow generated pad (Dmaj9, Bm9, Gmaj9, A add9) | generated | — |
| Voyager 1 | Golden Record: kiss, mother and child | `sounds/Kiss, Mother and Child.wav` | NASA/JPL, 1977 |
| Voyager 2 | Golden Record: footsteps, heartbeat, laughter | `sounds/Footsteps, Heartbeat, Laughter.wav` | NASA/JPL, 1977 |
| Voyager 2 (planned) | Humpback whales | not added yet | NOAA recording (public domain) suggested |
| Sgr A* (galactic centre) | Sonification of the Perseus cluster black hole (a stand-in) | `sounds/sonify5_perseus.mp3` | NASA/CXC/SAO/K. Arcand, M. Russo & A. Santaguida, CC BY-NC 3.0 |
| Moon | Apollo 11, "one small step" | `sounds/moon.mp3` | NASA, public domain |
| Mars | Perseverance's microphone | `sounds/mars.wav` | NASA/JPL-Caltech/LANL/CNES/CNRS/ISAE-SUPAERO |
| Radio ring | Marconi's 1901 Morse "S", re-created spark-gap sound | generated | — |
| Radio ring | Arecibo message as tones (1 = G5, 0 = E5) | generated | — |

Full credits: `sounds/CREDITS.md`. Check the Golden Record terms before publishing the site.
