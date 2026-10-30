"""Role-based pitch selection: root / fifth / octave / tension / approach, folded into the style's range."""
import random
from .core import Note


def _fit(p, low, high):
    while p > high and p - 12 >= low:
        p -= 12
    while p < low and p + 12 <= high:
        p += 12
    return p


def _segment_index(segs, step):
    for i, s in enumerate(segs):
        if s.start_step <= step < s.end_step:
            return i
    return len(segs) - 1


def assign_pitches(slots, segs, rng: random.Random, style):
    low, high = style.low, style.high
    roles, w = zip(*style.role_weights)
    seg_of = [_segment_index(segs, st) for st, _ in slots]
    last_in_seg = {si: i for i, si in enumerate(seg_of)}   # index of each segment's last slot
    root_of = lambda s: _fit(low + ((s.root - low) % 12), low, high)

    notes = []
    for i, ((step, length), si) in enumerate(zip(slots, seg_of)):
        seg = segs[si]
        # clip to the chord's end so notes don't bleed into the next chord, then apply gate
        length = max(1, min(length, seg.end_step - step))
        if length > 1:
            length = max(1, round(length * style.gate))
        root = root_of(seg)
        first = step == seg.start_step
        role = "root" if first else rng.choices(roles, w)[0]

        nxt = segs[(si + 1) % len(segs)]
        if (not first and last_in_seg[si] == i and style.approach_prob
                and nxt.root != seg.root and rng.random() < style.approach_prob):
            role = "approach"

        if role == "fifth":
            p = _fit(root + 7, low, high)
        elif role == "octave":
            p = _fit(root + 12, low, high)
            if p == root:       # no room above -> octave below if possible
                p = _fit(root - 12, low, high)
        elif role == "tension":  # b2 above the root
            p = _fit(root + 1, low, high)
        elif role == "approach":  # half step into the next chord's root, mostly from below
            nr = root_of(nxt)
            p = nr - 1 if rng.random() < 0.65 else nr + 1
            if p < low:
                p = nr + 1
            elif p > high:
                p = nr - 1
        else:
            p = root
        vel = style.vel_first if first else rng.randint(*style.vel_range)
        notes.append(Note(step, length, p, vel, role))
    return notes
