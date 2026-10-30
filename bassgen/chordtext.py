"""Typed chords -> ChordSegments.  'Am F7 C Gsus Dm:2'  (:N = N bars, default 1)"""
import re
from .core import ChordSegment, STEPS_PER_BAR

_LETTER = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
_ACC = {"": 0, "#": 1, "b": -1}
_RX = re.compile(r"^([A-Ga-g])([#b]?)([^:/]*)(?::(\d+))?$")


def parse_chord_text(text):
    toks = [t for t in re.split(r"[\s,|]+", text.strip()) if t]
    if not toks:
        raise ValueError("Akor listesi boş. Örnek: Am F C G")
    segs, pos = [], 0
    for t in toks:
        if "/" in t:
            raise ValueError(f"'{t}': slash akorlar henüz desteklenmiyor")
        m = _RX.match(t)
        if not m:
            raise ValueError(f"'{t}' akor olarak okunamadı. Örnek: Am, F#m7, Bb, Dm:2")
        letter, acc, suf, bars = m.groups()
        root = (_LETTER[letter.upper()] + _ACC[acc]) % 12
        s = suf.lower()
        if s.startswith("dim"):
            q, iv = "dim", [0, 3, 6]
        elif s.startswith("sus"):
            q, iv = "sus", [0, 5, 7]
        elif s.startswith("m") and not s.startswith("maj"):
            q, iv = "min", [0, 3, 7]
        else:
            q, iv = "maj", [0, 4, 7]
        if "maj7" in s:
            iv.append(11)
        elif "7" in s:
            iv.append(10)
        n = max(1, int(bars)) if bars else 1
        end = pos + n * STEPS_PER_BAR
        segs.append(ChordSegment(root, q, pos, end, tuple(sorted({(root + i) % 12 for i in iv}))))
        pos = end
    return segs
