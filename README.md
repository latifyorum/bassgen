# bassgen

Chord progression in, bassline MIDI out. bassgen takes a chord progression (typed or as a MIDI file) and writes many bassline variants for it, so you can audition them, pick one and edit it in your DAW. It is a block-breaker, not a replacement for writing the part yourself.

Türkçe: [README.tr.md](README.tr.md)

## Features

- Input: typed chords (`Am F7 C Gsus Dm:2`) or a chord MIDI file
- Genre presets: **trap (808)**, **rock**, **metal**, and a trap-rhythm + rock-notes **hybrid**
- Role-labelled notes (root, fifth, octave, approach, tension), folded into each style's register
- Local web UI: piano-roll preview, in-browser playback, MIDI download
- Seeded and reproducible: same seed, same result
- Pure Python, only dependency is [mido](https://github.com/mido/mido)

## Quick start

```bash
git clone https://github.com/latifyorum/bassgen.git
cd bassgen
pip install -e .

bassgen-web                       # opens http://127.0.0.1:8765
```

Command line:

```bash
bassgen --text "Am F C G" --style rock --n 8 --out out
bassgen --chords examples/am_f_c_g.mid --style metal --template gallop --bars 8 --seed 7
```

Without installing: `pip install mido`, then `python -m bassgen.web` or `python -m bassgen ...`.

## Styles

| Style | Rhythm | Notes | Register |
|---|---|---|---|
| `trap` | long 808-style notes with gaps, small fill every 4th bar | root, fifth, octave | E1-G2 |
| `rock` | 8th-note drive, pushes, syncopation | root, fifth, octave, half-step approach into the next chord | E1-D#3 |
| `metal` | pedal 8ths/16ths, gallops, chugs, short staccato notes | mostly root, rare b2 tension | C1-F2 |
| `hybrid` | trap rhythms | rock-style note choices | E1-C3 |

Styles are plain data in `bassgen/styles.py`; add your own by adding a `Style(...)` entry.

## How it works

```
chords -> parser -> rhythm (templates) -> pitch (roles) -> MIDI export
                          \_______ one Style preset drives every stage _______/
```

## Limitations and roadmap

- Root detection is a simple triad-template match; slash chords (`C/E`) are not supported yet
- Rhythm comes from templates only. Planned: lock the rhythm to a kick or guitar-riff MIDI
- Planned: variant scoring (kick collisions, consonance, density), slides and ghost notes for 808s

## License

MIT, see [LICENSE](LICENSE).
