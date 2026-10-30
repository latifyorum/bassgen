"""Note list -> MIDI (file or bytes)."""
import io
import mido


def build_midi(notes, bpm=140, tpb=480, channel=0):
    step_ticks = tpb // 4
    events = []
    for n in notes:
        on = n.step * step_ticks
        events.append((on, 1, mido.Message("note_on", note=n.pitch, velocity=n.velocity, channel=channel)))
        events.append((on + n.length * step_ticks, 0, mido.Message("note_off", note=n.pitch, velocity=0, channel=channel)))
    events.sort(key=lambda e: (e[0], e[1]))  # note_off before note_on at same tick

    mid = mido.MidiFile(ticks_per_beat=tpb)
    tr = mido.MidiTrack()
    mid.tracks.append(tr)
    tr.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(bpm), time=0))
    tr.append(mido.MetaMessage("track_name", name="bassgen", time=0))
    last = 0
    for tick, _, msg in events:
        tr.append(msg.copy(time=tick - last))
        last = tick
    return mid


def write_midi(notes, path, bpm=140, **kw):
    build_midi(notes, bpm, **kw).save(path)


def midi_bytes(notes, bpm=140, **kw):
    buf = io.BytesIO()
    build_midi(notes, bpm, **kw).save(file=buf)
    return buf.getvalue()
