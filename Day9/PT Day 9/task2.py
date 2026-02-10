from http.server import BaseHTTPRequestHandler, HTTPServer
import json
HOST = "localhost"
PORT = 8000
USERS = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
]


class UserAPI(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    def do_GET(self):
        parts = self.path.split("/")   # ["", "users", "1"]
        if len(parts) != 3 or parts[1] != "users":
            self.send_json(404, {"error": "Route not found"})
            return

        user_id = parts[2]
        if not user_id.isdigit():
            self.send_json(400, {"error": "User ID must be an integer"})
            return

        user_id = int(user_id)
        for user in USERS:
            if user["id"] == user_id:
                self.send_json(200, user)
                return
        self.send_json(404, {"error": "User not found"})


def run():
    server = HTTPServer((HOST, PORT), UserAPI)
    print(f"Server running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run()

# http://localhost:8000/users/1
# http://localhost:8000/users/abc
# http://localhost:8000/users/10