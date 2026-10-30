"""Template-based rhythm generator (kick/guitar-locked mode comes in step 2)."""
import random
from .core import STEPS_PER_BAR


def generate_rhythm(total_bars, rng: random.Random, style, template=None):
    """Return ([(step, length)], main_template_name). One main template; on every
    `fill_every`-th bar there is a chance of a different one (a small fill/variation)."""
    names = list(style.templates)
    main = template or rng.choices(names, [style.weights[n] for n in names])[0]
    slots = []
    for bar in range(total_bars):
        name = main
        if bar % style.fill_every == style.fill_every - 1 and rng.random() < style.fill_prob:
            name = rng.choice([n for n in names if n != main])
        for st, ln in style.templates[name]:
            slots.append((bar * STEPS_PER_BAR + st, ln))
    return slots, main
