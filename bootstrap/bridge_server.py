#!/usr/bin/env python3
"""BleakNarratives <-> OpenHands drive bridge.

Serves /workspace/bridge/outbox for download and accepts uploads into
/workspace/bridge/inbox. Single file, stdlib only, Termux/Crostini safe.
"""
import email.parser
import email.policy
import html
import http.server
import os
import socketserver
import urllib.parse
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "outbox")
INBOX = os.path.join(ROOT, "inbox")
os.makedirs(OUT, exist_ok=True)
os.makedirs(INBOX, exist_ok=True)
PORT = int(os.environ.get("BRIDGE_PORT", "12000"))

PAGE = """<!doctype html><meta charset=utf-8><title>drive bridge</title>
<style>
body{{font:14px/1.6 ui-monospace,monospace;background:#111;color:#ddd;padding:24px;max-width:900px}}
h1{{font-size:17px}} a{{color:#7fd}} code{{background:#222;padding:2px 6px;border-radius:4px}}
li{{margin:3px 0;list-style:none}} .k{{color:#8f8}} .d{{color:#666}}
</style>
<h1>drive bridge &middot; {now}</h1>
<h3>outbox &mdash; pull these to the Chromebook</h3><ul>{out}</ul>
<h3>inbox &mdash; files pushed from the Chromebook</h3><ul>{inbox}</ul>
<h3>push a file from the Chromebook</h3>
<pre><code>curl -sS -F "file=@/path/to/local.txt" {base}upload</code></pre>
<h3>pull a file to the Chromebook</h3>
<pre><code>curl -sS {base}outbox/FILENAME -o ~/FILENAME</code></pre>
<p class=d>uploads land in /workspace/bridge/inbox on the OpenHands side.</p>
"""


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def log_message(self, fmt, *args):
        with open(os.path.join(ROOT, "bridge_access.log"), "a") as fh:
            fh.write(f"{datetime.now().isoformat()} {self.address_string()} {fmt % args}\n")

    def _listing(self, directory, prefix):
        rows = []
        for name in sorted(os.listdir(directory)):
            path = os.path.join(directory, name)
            if os.path.isfile(path):
                rows.append(
                    f'<li><a href="{prefix}{urllib.parse.quote(name)}">'
                    f'{html.escape(name)}</a> '
                    f'<span class="k">{os.path.getsize(path):,}B</span></li>'
                )
        return "".join(rows) or "<li class='d'>empty</li>"

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            base = f"http://{self.headers.get('Host', 'localhost')}/"
            body = PAGE.format(
                now=datetime.now().strftime("%Y-%m-%d %H:%M"),
                out=self._listing(OUT, "/outbox/"),
                inbox=self._listing(INBOX, "/inbox/"),
                base=base,
            ).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path.startswith("/inbox/"):
            self.send_error(403, "inbox is write-only")
            return
        return super().do_GET()

    def do_POST(self):
        if not self.path.startswith("/upload"):
            self.send_error(404)
            return
        ctype = self.headers.get("Content-Type", "")
        name = ""
        data = b""
        if ctype.startswith("multipart/form-data"):
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            msg = email.parser.BytesParser(policy=email.policy.default).parsebytes(
                b"Content-Type: " + ctype.encode() + b"\r\n\r\n" + raw
            )
            for part in msg.iter_parts():
                if part.get_param("name", header="content-disposition") == "file":
                    name = part.get_filename() or ""
                    data = part.get_payload(decode=True) or b""
                    break
        else:
            name = os.path.basename(
                urllib.parse.unquote(self.path[len("/upload"):].lstrip("/"))
            )
            data = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        if not name:
            name = "upload-" + datetime.now().strftime("%Y%m%d-%H%M%S")
        safe = os.path.basename(name).replace("..", "_")
        dest = os.path.join(INBOX, safe)
        with open(dest, "wb") as fh:
            fh.write(data)
        body = f"stored {safe} ({len(data):,}B)\n".encode()
        self.send_response(201)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    print(f"bridge up on 0.0.0.0:{PORT}  root={ROOT}")
    Server(("0.0.0.0", PORT), Handler).serve_forever()
