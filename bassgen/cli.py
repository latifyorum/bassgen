import argparse, os
from .core import parse_chords, prog_bars
from .chordtext import parse_chord_text
from .styles import STYLES
from .service import generate_variants
from .export import write_midi


def main():
    ap = argparse.ArgumentParser(prog="bassgen", description="Chord MIDI -> bassline MIDI")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--chords", help="chord progression .mid")
    g.add_argument("--text", help="typed chords, e.g. 'Am F C G'")
    ap.add_argument("--bars", type=int, default=0, help="phrase length (default: progression length)")
    ap.add_argument("--n", type=int, default=8, help="number of variants")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--style", choices=list(STYLES), default="trap", help="genre preset")
    ap.add_argument("--template", help="force a rhythm template of the chosen style")
    ap.add_argument("--bpm", type=int, help="override tempo")
    ap.add_argument("--out", default="out")
    a = ap.parse_args()

    if a.chords:
        segs, bpm = parse_chords(a.chords)
    else:
        segs, bpm = parse_chord_text(a.text), 140
    bpm = a.bpm or bpm
    bars = a.bars or prog_bars(segs)
    segs, variants = generate_variants(segs, bars, a.n, a.seed, a.style, a.template)
    os.makedirs(a.out, exist_ok=True)

    print(f"{a.style}: {len(segs)} chord segments, {bars} bars, {bpm} BPM")
    for i, (tpl, notes) in enumerate(variants):
        path = os.path.join(a.out, f"bass_{i + 1:02d}.mid")
        write_midi(notes, path, bpm)
        print(f"  {path}  template={tpl:8s} notes={len(notes)}")


if __name__ == "__main__":
    main()
