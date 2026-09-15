#!/usr/bin/env python3
"""Static server for corporate/ that forbids caching. python -m http.server sends
Last-Modified and browsers then reuse HTML heuristically, so a regenerated page can
sit behind a stale copy for minutes. Every response here is no-store."""
import http.server, os, sys
PORT = int(os.environ.get("PORT") or (sys.argv[1] if len(sys.argv) > 1 else 8899))
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Pragma", "no-cache"); self.send_header("Expires", "0")
        super().end_headers()
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(("", PORT), H).serve_forever()
