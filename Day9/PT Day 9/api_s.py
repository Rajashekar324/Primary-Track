from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs
import json

HOST = "localhost"
PORT = 8000

# ✅ Store last POSTed data
last_post_data = {}


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


class SimpleAPI(BaseHTTPRequestHandler):

    def _send_response(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    # ✅ GET should return last POST data
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path != "/echo":
            self._send_response(404, {"error": "Not found"})
            return

        # If nothing posted yet
        if not last_post_data:
            self._send_response(200, {"message": "No POST data yet"})
            return

        self._send_response(200, last_post_data)

    # ❌ POST OUTPUT NOT CHANGED
    def do_POST(self):
        global last_post_data  # ✅ allow modification

        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path != "/echo":
            self._send_response(404, {"error": "Not found"})
            return

        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)

        if raw_body:
            try:
                body = json.loads(raw_body)
                last_post_data = body  # ✅ store POST data
            except json.JSONDecodeError:
                self._send_response(400, {"error": "Invalid JSON"})
                return
        else:
            body = {}

        # ✅ POST RESPONSE REMAINS EXACTLY SAME
        self._send_response(200, {
            "path": path,
            "query": query,
            "body": body
        })


def run():
    server = ThreadedHTTPServer((HOST, PORT), SimpleAPI)
    print(f"Server running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run()