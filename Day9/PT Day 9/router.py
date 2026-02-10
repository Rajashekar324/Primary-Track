from http.server import BaseHTTPRequestHandler, HTTPServer
import json

HOST = "localhost"
PORT = 8000


# ----------------------
# Router
# ----------------------
ROUTES = {
    ("GET", "/"): "home",
    ("GET", "/health"): "health",
    ("GET", "/users"): "get_users",
    ("POST", "/users"): "create_user",
}


class SimpleAPI(BaseHTTPRequestHandler):

    # -------- Helpers --------
    def send_json(self, status=200, data=None):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if data is not None:
            self.wfile.write(json.dumps(data).encode())

    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        body = self.rfile.read(length)
        return json.loads(body)

    # -------- Router --------
    def handle_route(self):
        route = (self.command, self.path)
        handler_name = ROUTES.get(route)

        if not handler_name:
            self.send_json(404, {"error": "Route not found"})
            return

        handler = getattr(self, handler_name)
        handler()

    # -------- HTTP methods --------
    def do_GET(self):
        self.handle_route()

    def do_POST(self):
        self.handle_route()

    # -------- Controllers --------
    def home(self):
        self.send_json(200, {"message": "API running"})

    def health(self):
        self.send_json(200, {"status": "ok"})

    def get_users(self):
        users = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ]
        self.send_json(200, users)

    def create_user(self):
        try:
            data = self.read_json()
        except json.JSONDecodeError:
            self.send_json(400, {"error": "Invalid JSON"})
            return

        user = {
            "id": 3,
            "name": data.get("name")
        }
        self.send_json(201, user)


def run():
    server = HTTPServer((HOST, PORT), SimpleAPI)
    print(f"Server running on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run()