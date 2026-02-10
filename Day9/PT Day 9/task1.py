from http.server import BaseHTTPRequestHandler, HTTPServer
import json

HOST = "localhost"
PORT = 8000

# In-memory storage
NOTES = []


class NotesAPI(BaseHTTPRequestHandler):

    # ---------- Helper ----------
    def send_json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return None
        body = self.rfile.read(length)
        return json.loads(body)

    # ---------- GET ----------
    def do_GET(self):
        if self.path != "/notes":
            self.send_json(404, {"error": "Route not found"})
            return

        self.send_json(200, NOTES)

    # ---------- POST ----------
    def do_POST(self):
        if self.path != "/notes":
            self.send_json(404, {"error": "Route not found"})
            return

        try:
            data = self.read_json()
        except json.JSONDecodeError:
            self.send_json(400, {"error": "Invalid JSON"})
            return

        # Validate JSON key
        if not data or "text" not in data:
            self.send_json(400, {"error": "text field is required"})
            return

        note = {
            "id": len(NOTES) + 1,
            "text": data["text"]
        }

        NOTES.append(note)
        self.send_json(201, note)


def run():
    server = HTTPServer((HOST, PORT), NotesAPI)
    print(f"Server running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run()

#POST http://localhost:8000/notes
#Content-Type: application/json
#{
#    "text": "This is a note"   
#}