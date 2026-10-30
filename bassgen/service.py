"""One place that runs the pipeline; used by both the CLI and the web UI."""
import random
from .core import loop_segments
from .rhythm import generate_rhythm
from .pitch import assign_pitches
from .styles import get_style


def generate_variants(segs, bars, n, seed, style="trap", template=None):
    style = get_style(style) if isinstance(style, str) else style
    if template and template not in style.templates:
        raise ValueError(f"'{template}' şablonu {style.id} stilinde yok. Seçenekler: {', '.join(style.templates)}")
    segs = loop_segments(segs, bars)
    out = []
    for i in range(n):
        rng = random.Random(seed + i)
        slots, tpl = generate_rhythm(bars, rng, style, template)
        out.append((tpl, assign_pitches(slots, segs, rng, style)))
    return segs, out
