"""Local web UI:  python -m bassgen.web   (stdlib only, no extra install)"""
import argparse, base64, json, os, tempfile, webbrowser
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .core import parse_chords, prog_bars
from .chordtext import parse_chord_text
from .styles import STYLES, get_style
from .service import generate_variants
from .export import midi_bytes

HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
SUFFIX = {"maj": "", "min": "m", "dim": "dim", "sus": "sus"}


def _int(v, default, lo, hi):
    try:
        return max(lo, min(hi, int(v)))
    except (TypeError, ValueError):
        return default


def api_generate(p):
    bpm_in = p.get("bpm")
    if p.get("midi_b64"):
        with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as f:
            f.write(base64.b64decode(p["midi_b64"]))
            path = f.name
        try:
            segs, bpm = parse_chords(path)
        finally:
            os.unlink(path)
    else:
        segs, bpm = parse_chord_text(p.get("chords", "")), 140
    bpm = _int(bpm_in, bpm, 40, 300)
    bars = _int(p.get("bars"), prog_bars(segs), 1, 64)
    n = _int(p.get("n"), 8, 1, 32)
    seed = _int(p.get("seed"), 42, 0, 10**9)
    style = get_style(p.get("style") or "trap")
    tpl = p.get("template") or None

    segs, variants = generate_variants(segs, bars, n, seed, style, tpl)
    return {
        "bpm": bpm, "bars": bars, "style": style.label,
        "chords": [{"start": s.start_step, "end": s.end_step, "pcs": list(s.pcs),
                    "label": NAMES[s.root] + SUFFIX[s.quality]} for s in segs],
        "variants": [{"template": t, "notes": [asdict(x) for x in notes],
                      "midi_b64": base64.b64encode(midi_bytes(notes, bpm)).decode()}
                     for t, notes in variants],
    }


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/api/meta":
            self._send(200, {"styles": [{"id": s.id, "label": s.label, "templates": list(s.templates)} for s in STYLES.values()]})
        elif self.path in ("/", "/index.html"):
            with open(os.path.join(HERE, "web_ui.html"), "rb") as f:
                self._send(200, f.read(), "text/html")
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/api/generate":
            return self._send(404, {"error": "not found"})
        try:
            size = int(self.headers.get("Content-Length", 0))
            self._send(200, api_generate(json.loads(self.rfile.read(size) or b"{}")))
        except Exception as e:  # shown in the UI as-is
            self._send(400, {"error": str(e)})

    def log_message(self, *a):
        pass


def main():
    ap = argparse.ArgumentParser(prog="bassgen.web")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-browser", action="store_true")
    a = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), Handler)
    url = f"http://127.0.0.1:{a.port}"
    print(f"bassgen arayüzü: {url}  (kapatmak için Ctrl+C)")
    if not a.no_browser:
        webbrowser.open(url)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
