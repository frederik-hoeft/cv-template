"""Simple HTTP server that rewrites file:// references to CDN URLs in HTML responses."""

import io
import os
import re
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

REWRITES = [
    (
        re.compile(r'file:///+[^"]*?/katex/katex\.min\.css'),
        "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css",
    ),
]


class RewritingHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith((".html", ".htm")):
            self._serve_rewritten_html()
        else:
            super().do_GET()

    def _serve_rewritten_html(self):
        path = self.translate_path(self.path)
        try:
            with open(path, "rb") as f:
                content = f.read()
        except OSError:
            self.send_error(404, "File not found")
            return

        text = content.decode("utf-8", errors="replace")
        for pattern, replacement in REWRITES:
            text = pattern.sub(replacement, text)
        encoded = text.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(encoded)


if __name__ == "__main__":
    import sys

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    directory = sys.argv[2] if len(sys.argv) > 2 else "."

    import os
    os.chdir(directory)

    server = HTTPServer(("", port), RewritingHandler)
    print(f"Serving on port {port} from {directory}")
    server.serve_forever()
