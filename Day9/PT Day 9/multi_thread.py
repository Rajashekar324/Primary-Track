from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs
import json
import threading

HOST = "localhost"
PORT = 8000


ROUTES = {
    ("GET", "/users"): "get_users",
    ("POST", "/users"): "create_user",
}


# -------- Multithreaded Server --------
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


class SimpleAPI(BaseHTTPRequestHandler):

    # -------- Response helpers --------
    def send_json(self, status_code, data=None):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if data is not None:
            self.wfile.write(json.dumps(data).encode())

    # -------- Request helpers --------
    def parse_path(self):
        parsed = urlparse(self.path)
        return parsed.path, parse_qs(parsed.query)

    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            raise ValueError("Empty body")
        return json.loads(self.rfile.read(length))

    # -------- Router --------
    def handle_route(self):
        path, _ = self.parse_path()
        route = (self.command, path)

        handler_name = ROUTES.get(route)
        if not handler_name:
            self.send_json(404, {"error": "Route not found"})
            return

        try:
            getattr(self, handler_name)()
        except ValueError as e:
            self.send_json(400, {"error": str(e)})
        except json.JSONDecodeError:
            self.send_json(400, {"error": "Invalid JSON"})
        except Exception:
            self.send_json(500, {"error": "Internal server error"})

    # -------- HTTP methods --------
    def do_GET(self):
        self.handle_route()

    def do_POST(self):
        self.handle_route()

    # -------- Controllers --------
    def get_users(self):
        thread = threading.current_thread().name

        users = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ]

        self.send_json(200, {
            "thread": thread,
            "data": users
        })

    def create_user(self):
        data = self.read_json()

        if "name" not in data:
            raise ValueError("`name` is required")

        self.send_json(201, {
            "id": 3,
            "name": data["name"]
        })


def run():
    server = ThreadedHTTPServer((HOST, PORT), SimpleAPI)
    print(f"Multithreaded server running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run()
'''
curl http://localhost:8000/users &
curl http://localhost:8000/users &
curl http://localhost:8000/users &
'''