"""Shared data model + chord MIDI parser."""
from dataclasses import dataclass, field
import math
import mido

STEPS_PER_BAR = 16  # 16th-note grid


@dataclass
class ChordSegment:
    root: int          # pitch class 0-11
    quality: str       # maj / min / dim / sus
    start_step: int
    end_step: int      # exclusive
    pcs: tuple = field(default_factory=tuple)  # all pitch classes in chord


@dataclass
class Note:
    step: int
    length: int        # in steps
    pitch: int         # MIDI note number
    velocity: int = 100
    role: str = "root"


def _detect_root_quality(pitches):
    """Pick the root by simple triad-template scoring; ties go to the lowest note."""
    pcs = sorted({p % 12 for p in pitches})
    lowest_pc = min(pitches) % 12
    best = None
    for cand in pcs:
        iv = {(pc - cand) % 12 for pc in pcs}
        score = 3 * (7 in iv) + 3 * (3 in iv or 4 in iv) + (10 in iv or 11 in iv)
        score += 0.5 if cand == lowest_pc else 0
        if best is None or score > best[0]:
            best = (score, cand, iv)
    _, root, iv = best
    if 3 in iv and 6 in iv and 7 not in iv:
        q = "dim"
    elif 3 in iv:
        q = "min"
    elif 4 in iv:
        q = "maj"
    else:
        q = "sus"
    return root, q, tuple(pcs)


def parse_chords(path, default_bpm=140):
    """Read a chord-progression MIDI -> (segments, bpm). Notes starting on the
    same 16th step form one chord; it lasts until the next chord onset."""
    mid = mido.MidiFile(path)
    tpb = mid.ticks_per_beat
    step_ticks = tpb / 4
    bpm = default_bpm
    open_notes, notes = {}, []  # notes: (start_tick, end_tick, pitch)
    t = 0
    for msg in mido.merge_tracks(mid.tracks):
        t += msg.time
        if msg.type == "set_tempo":
            bpm = round(mido.tempo2bpm(msg.tempo))
        elif msg.type == "note_on" and msg.velocity > 0:
            open_notes[(msg.channel, msg.note)] = t
        elif msg.type in ("note_off", "note_on"):
            s = open_notes.pop((msg.channel, msg.note), None)
            if s is not None:
                notes.append((s, t, msg.note))
    if not notes:
        raise ValueError("No notes found in chord MIDI")

    groups = {}
    for s, e, p in notes:
        groups.setdefault(round(s / step_ticks), []).append(p)
    onsets = sorted(groups)
    end_all = max(round(e / step_ticks) for _, e, _ in notes)
    segs = []
    for i, st in enumerate(onsets):
        en = onsets[i + 1] if i + 1 < len(onsets) else end_all
        root, q, pcs = _detect_root_quality(groups[st])
        segs.append(ChordSegment(root, q, st, max(en, st + 1), pcs))
    return segs, bpm


def prog_bars(segs):
    return math.ceil(max(s.end_step for s in segs) / STEPS_PER_BAR)


def loop_segments(segs, total_bars):
    """Tile the progression to cover total_bars."""
    n = prog_bars(segs)
    out, rep = [], 0
    while rep * n < total_bars:
        off = rep * n * STEPS_PER_BAR
        limit = total_bars * STEPS_PER_BAR
        for s in segs:
            if s.start_step + off >= limit:
                continue
            out.append(ChordSegment(s.root, s.quality, s.start_step + off,
                                    min(s.end_step + off, limit), s.pcs))
        rep += 1
    return out
