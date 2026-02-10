from http.server import BaseHTTPRequestHandler, HTTPServer
import json

users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
    {"id": 4, "name": "David"},
    {"id": 5, "name": "Eve"},
    {"id": 6, "name": "Frank"}
]


class API(BaseHTTPRequestHandler):

    def send_json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    # 🔹 GET users / users/{id}
    def do_GET(self):
        parts = self.path.strip("/").split("/")

        # GET /users
        if len(parts) == 1 and parts[0] == "users":
            self.send_json(200, users)
            return

        # GET /users/{id}
        if len(parts) == 2 and parts[0] == "users":
            if not parts[1].isdigit():
                self.send_json(400, {"error": "Invalid user id"})
                return

            user_id = int(parts[1])
            for user in users:
                if user["id"] == user_id:
                    self.send_json(200, user)
                    return

            self.send_json(404, {"error": "User not found"})
            return

        self.send_json(404, {"error": "Route not found"})

    # 🔹 PUT /users/{id}
    def do_PUT(self):
        parts = self.path.strip("/").split("/")

        if len(parts) != 2 or parts[0] != "users":
            self.send_json(404, {"error": "Route not found"})
            return

        if not parts[1].isdigit():
            self.send_json(400, {"error": "Invalid user id"})
            return

        user_id = int(parts[1])

        length = self.headers.get("Content-Length")
        if not length:
            self.send_json(400, {"error": "Missing request body"})
            return

        try:
            data = json.loads(self.rfile.read(int(length)))
        except json.JSONDecodeError:
            self.send_json(400, {"error": "Invalid JSON"})
            return

        if "name" not in data or not data["name"]:
            self.send_json(400, {"error": "`name` is required"})
            return

        for user in users:
            if user["id"] == user_id:
                user["name"] = data["name"]
                self.send_json(200, user)
                return

        self.send_json(404, {"error": "User not found"})

    # 🔹 DELETE /users/{id}
    def do_DELETE(self):
        parts = self.path.strip("/").split("/")

        if len(parts) != 2 or parts[0] != "users":
            self.send_json(404, {"error": "Route not found"})
            return

        if not parts[1].isdigit():
            self.send_json(400, {"error": "Invalid user id"})
            return

        user_id = int(parts[1])

        for user in users:
            if user["id"] == user_id:
                users.remove(user)
                self.send_json(200, {"message": "User deleted"})
                return

        self.send_json(404, {"error": "User not found"})


HTTPServer(("localhost", 8000), API).serve_forever()
# http://localhost:8000/users/1