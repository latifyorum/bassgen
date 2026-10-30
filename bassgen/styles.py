"""Genre presets. A Style is pure data: swap it and the same pipeline writes a different kind of bassline.
One-bar templates live on a 16th grid: (start_step, length_in_steps)."""
from dataclasses import dataclass

_EIGHTHS = [(i, 2) for i in range(0, 16, 2)]
_SIXTEENTHS = [(i, 1) for i in range(16)]


@dataclass(frozen=True)
class Style:
    id: str
    label: str
    templates: dict
    weights: dict
    role_weights: tuple          # roles picked for notes that aren't a chord's first note
    low: int                     # register (MIDI note numbers)
    high: int
    gate: float = 1.0            # note-length multiplier (<1 = shorter, more staccato)
    approach_prob: float = 0.0   # chance the last note before a chord change leads into the next root
    vel_first: int = 110         # velocity on a chord's first note
    vel_range: tuple = (88, 104)
    fill_prob: float = 0.6       # chance of a different template on every 4th bar
    fill_every: int = 4


TRAP_TEMPLATES = {
    "sustain": [(0, 16)],
    "half":    [(0, 8), (8, 8)],
    "trap_a":  [(0, 6), (7, 1), (10, 4), (14, 2)],
    "trap_b":  [(0, 3), (3, 3), (8, 5), (13, 3)],
    "trap_c":  [(0, 10), (10, 2), (12, 4)],
    "trap_d":  [(0, 2), (4, 2), (6, 2), (10, 6)],
    "bounce":  [(0, 4), (6, 2), (8, 4), (14, 2)],
}
TRAP_WEIGHTS = {"sustain": 1, "half": 1, "trap_a": 3, "trap_b": 3, "trap_c": 2, "trap_d": 2, "bounce": 3}

ROCK_TEMPLATES = {
    "eighths":  _EIGHTHS,
    "quarters": [(0, 4), (4, 4), (8, 4), (12, 4)],
    "push":     [(0, 4), (4, 2), (6, 2), (8, 4), (12, 2), (14, 2)],
    "syncop":   [(0, 3), (3, 3), (6, 2), (8, 2), (10, 2), (12, 4)],
    "half_run": [(0, 8), (8, 4), (12, 4)],
    "dotted":   [(0, 6), (6, 2), (8, 6), (14, 2)],
}
ROCK_WEIGHTS = {"eighths": 4, "quarters": 1, "push": 3, "syncop": 3, "half_run": 1, "dotted": 2}

METAL_TEMPLATES = {
    "pedal_8":    _EIGHTHS,
    "pedal_16":   _SIXTEENTHS,
    "gallop":     [(b + o, l) for b in range(0, 16, 4) for o, l in ((0, 2), (2, 1), (3, 1))],
    "gallop_rev": [(b + o, l) for b in range(0, 16, 4) for o, l in ((0, 1), (1, 1), (2, 2))],
    "chug":       [(0, 2), (2, 1), (4, 2), (6, 1), (8, 2), (10, 2), (12, 1), (14, 2)],
    "break":      [(0, 6), (8, 2), (10, 2), (12, 4)],
}
METAL_WEIGHTS = {"pedal_8": 4, "pedal_16": 2, "gallop": 3, "gallop_rev": 2, "chug": 3, "break": 1}

STYLES = {s.id: s for s in [
    Style("trap", "Trap (808)", TRAP_TEMPLATES, TRAP_WEIGHTS,
          (("root", 0.6), ("fifth", 0.2), ("octave", 0.2)), low=28, high=43),
    Style("rock", "Rock", ROCK_TEMPLATES, ROCK_WEIGHTS,
          (("root", 0.55), ("fifth", 0.2), ("octave", 0.25)), low=28, high=51,
          gate=0.9, approach_prob=0.5, vel_first=100, vel_range=(80, 100), fill_prob=0.5),
    Style("metal", "Metal", METAL_TEMPLATES, METAL_WEIGHTS,
          (("root", 0.86), ("fifth", 0.06), ("octave", 0.04), ("tension", 0.04)), low=24, high=41,
          gate=0.55, approach_prob=0.1, vel_first=118, vel_range=(106, 120), fill_prob=0.3),
    # example of mixing presets: trap rhythm + rock note choices
    Style("hybrid", "Trap ritmi + rock notaları", TRAP_TEMPLATES, TRAP_WEIGHTS,
          (("root", 0.55), ("fifth", 0.2), ("octave", 0.25)), low=28, high=48,
          gate=0.95, approach_prob=0.4),
]}


def get_style(name):
    if name not in STYLES:
        raise ValueError(f"Bilinmeyen stil: {name}. Seçenekler: {', '.join(STYLES)}")
    return STYLES[name]
