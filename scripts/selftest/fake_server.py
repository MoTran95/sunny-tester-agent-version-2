"""Fake app for self-testing the automation library: login form, HttpOnly session cookie, /api/me, sign-out.

Runs only on localhost with fake accounts; never touches the real system under test.
"""
import json
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ACCOUNTS = {"P1": "fake-pass-1", "P2": "fake-pass-2"}

PAGE = """<!doctype html><meta charset=utf-8><title>Fake</title><div id=app>Đang tải…</div>
<script>
async function load(){
  await new Promise(r => setTimeout(r, 800));
  const me = await fetch('/api/me');
  const app = document.getElementById('app');
  if (me.status === 200) {
    const d = await me.json();
    app.innerHTML = '<header>Fake | Danh sách việc | ' + d.employeeId + ' · Chuyên viên giả · DEFAULT | <button id=out>Đăng xuất</button></header><main><h1>Danh sách việc</h1></main>';
    document.getElementById('out').onclick = async () => { await fetch('/api/auth/sign-out', {method: 'POST'}); location.reload(); };
  } else {
    app.innerHTML = '<form id=f><label>Tên đăng nhập *<input name=u></label><label>Mật khẩu *<input type=password name=p></label><button type=submit>Đăng nhập</button></form>';
    document.getElementById('f').onsubmit = async (e) => { e.preventDefault();
      const r = await fetch('/api/auth/sign-in', {method: 'POST', headers: {'content-type': 'application/json'}, body: JSON.stringify({employeeId: f.u.value, password: f.p.value})});
      if (r.status === 200) location.reload(); };
  }
}
load();
</script>"""


class Handler(BaseHTTPRequestHandler):
    sessions = set()

    def log_message(self, *args):
        pass

    def _send(self, status, body=b"", content_type="application/json", cookie=None):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(body)

    def _sid(self):
        for part in self.headers.get("Cookie", "").split(";"):
            part = part.strip()
            if part.startswith("sid="):
                return part[4:]
        return None

    def do_GET(self):
        if self.path == "/api/me":
            sid = self._sid()
            if sid in Handler.sessions:
                self._send(200, json.dumps({"employeeId": sid.split(".")[0], "role": "FAKE"}).encode())
            else:
                self._send(401, b'{"error":"auth.required"}')
        else:
            self._send(200, PAGE.encode("utf-8"), "text/html; charset=utf-8")

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        if self.path == "/api/auth/sign-in":
            data = json.loads(body or b"{}")
            if ACCOUNTS.get(data.get("employeeId")) == data.get("password"):
                sid = f"{data['employeeId']}.{len(Handler.sessions)}"
                Handler.sessions.add(sid)
                self._send(200, b"{}", cookie=f"sid={sid}; HttpOnly; Path=/")
            else:
                self._send(401, b'{"error":"auth.invalidCredentials"}')
        elif self.path == "/api/auth/sign-out":
            Handler.sessions.discard(self._sid())
            self._send(204)
        else:
            self._send(404)


def start():
    """Start the server on a free port in a background thread. Returns (server, base_url)."""
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{port}"
