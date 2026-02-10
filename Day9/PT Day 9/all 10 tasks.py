# ## 4️⃣ Test each task (Postman / curl)

# ---

# ## ✅ Task 1: Health Check

# **GET**

# ```
# http://localhost:8000/health
# ```

# **Output**

# ```json
# {
#   "status": "ok"
# }
# ```

# ---

# ## ✅ Task 2: Create Note

# **POST**

# ```
# http://localhost:8000/notes
# ```

# **Headers**

# ```
# Content-Type: application/json
# ```

# **Body → raw → JSON**

# ```json
# {
#   "text": "hello"
# }
# ```

# **Output (201)**

# ```json
# {
#   "id": 1,
#   "text": "hello"
# }
# ```

# ---

# ## ✅ Task 3: List Notes

# **GET**

# ```
# http://localhost:8000/notes
# ```

# **Output**

# ```json
# [
#   {
#     "id": 1,
#     "text": "hello"
#   }
# ]
# ```

# ---

# ## ✅ Task 4: Get Note by ID

# **GET**

# ```
# http://localhost:8000/notes/1
# ```

# **Output**

# ```json
# {
#   "id": 1,
#   "text": "hello"
# }
# ```

# ---

# ## ✅ Task 5: Update Note

# **PUT**

# ```
# http://localhost:8000/notes/1
# ```

# **Headers**

# ```
# Content-Type: application/json
# ```

# **Body**

# ```json
# {
#   "text": "updated note"
# }
# ```

# **Output**

# ```json
# {
#   "id": 1,
#   "text": "updated note"
# }
# ```

# ---

# ## ✅ Task 6: Delete Note

# **DELETE**

# ```
# http://localhost:8000/notes/1
# ```

# **Output**

# * Status: **204 No Content**
# * No body (this is correct)

# ---

# ## ✅ Task 7: Search Notes

# First create some notes:

# ```json
# hello world
# python api
# hello server
# ```

# **GET**

# ```
# http://localhost:8000/notes?search=hello
# ```

# **Output**

# ```json
# [
#   {"id": 1, "text": "hello world"},
#   {"id": 3, "text": "hello server"}
# ]
# ```

# ---

# ## ✅ Task 8: API Key Auth

# **GET**

# ```
# http://localhost:8000/secret
# ```

# ### Headers (VERY IMPORTANT)

# | Key       | Value    |
# | --------- | -------- |
# | X-API-Key | mykey123 |

# **Output**

# ```json
# {
#   "message": "Secret data"
# }
# ```

# ❌ Without header → `401 Unauthorized`

# ---

# ## ✅ Task 9: Rate Limiter

# Call **any endpoint more than 5 times in 1 minute**:

# ```bash
# for i in {1..10}; do curl http://localhost:8000/health; done
# ```

# **Output**

# ```json
# {
#   "error": "Too many requests"
# }
# ```

# Status: **429**

# ---

# ## ✅ Task 10: Graceful Shutdown

# **POST**

# ```
# http://localhost:8000/shutdown
# ```

# ⚠️ Must be from **same machine** (127.0.0.1)

# **Output**

# ```json
# {
#   "message": "Server shutting down"
# }
# ```
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json, time

HOST = "localhost"
PORT = 8000

notes = []          # In-memory storage for notes
request_log = {}    # Used for rate limiting (Task 9)
API_KEY = "mykey123"  # API key for authentication (Task 8)


class API(BaseHTTPRequestHandler):

    # ---------- Helper: Send JSON response ----------
    def send_json(self, status, data=None):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if data is not None:
            self.wfile.write(json.dumps(data).encode())

    # ---------- Helper: Read JSON body ----------
    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return None
        return json.loads(self.rfile.read(length))

    # ---------- Task 9: Rate Limiter ----------
    # Max 5 requests per minute per IP
    def rate_limit(self):
        ip = self.client_address[0]
        now = time.time()

        requests = request_log.get(ip, [])
        requests = [t for t in requests if now - t < 60]

        if len(requests) >= 5:
            self.send_json(429, {"error": "Too many requests"})
            return False

        requests.append(now)
        request_log[ip] = requests
        return True

    # ---------- GET Requests ----------
    def do_GET(self):
        if not self.rate_limit():
            return

        parsed = urlparse(self.path)
        parts = parsed.path.strip("/").split("/")
        query = parse_qs(parsed.query)

        # ---------- Task 1: Health Check ----------
        # GET /health
        if self.path == "/health":
            self.send_json(200, {"status": "ok"})
            return

        # ---------- Task 8: API Key Authentication ----------
        # GET /secret (Requires X-API-Key header)
        if self.path == "/secret":
            if self.headers.get("X-API-Key") != API_KEY:
                self.send_json(401, {"error": "Unauthorized"})
                return
            self.send_json(200, {"message": "Secret data"})
            return

        # ---------- Task 3: List Notes ----------
        # ---------- Task 7: Search Notes ----------
        # GET /notes or GET /notes?search=word
        if parts[0] == "notes" and len(parts) == 1:
            search = query.get("search", [None])[0]
            result = notes

            if search:
                result = [
                    n for n in notes
                    if search.lower() in n["text"].lower()
                ]

            self.send_json(200, result)
            return

        # ---------- Task 4: Get Note by ID ----------
        # GET /notes/{id}
        if parts[0] == "notes" and len(parts) == 2:
            if not parts[1].isdigit():
                self.send_json(400, {"error": "Invalid ID"})
                return

            note_id = int(parts[1])
            for note in notes:
                if note["id"] == note_id:
                    self.send_json(200, note)
                    return

            self.send_json(404, {"error": "Note not found"})
            return

        self.send_json(404, {"error": "Route not found"})

    # ---------- POST Requests ----------
    def do_POST(self):
        if not self.rate_limit():
            return

        # ---------- Task 2: Create Note ----------
        # POST /notes
        if self.path == "/notes":
            try:
                data = self.read_json()
            except:
                self.send_json(400, {"error": "Invalid JSON"})
                return

            if not data or "text" not in data:
                self.send_json(400, {"error": "Text is required"})
                return

            note = {
                "id": len(notes) + 1,
                "text": data["text"]
            }
            notes.append(note)
            self.send_json(201, note)
            return

        # ---------- Task 10: Graceful Shutdown ----------
        # POST /shutdown (Only from localhost)
        if self.path == "/shutdown":
            if self.client_address[0] != "127.0.0.1":
                self.send_json(403, {"error": "Forbidden"})
                return

            self.send_json(200, {"message": "Server shutting down"})
            self.server.shutdown()
            return

        self.send_json(404, {"error": "Route not found"})

    # ---------- PUT Requests ----------
    def do_PUT(self):
        if not self.rate_limit():
            return

        parts = self.path.strip("/").split("/")

        # ---------- Task 5: Update Note ----------
        # PUT /notes/{id}
        if len(parts) == 2 and parts[0] == "notes":
            if not parts[1].isdigit():
                self.send_json(400, {"error": "Invalid ID"})
                return

            note_id = int(parts[1])

            try:
                data = self.read_json()
            except:
                self.send_json(400, {"error": "Invalid JSON"})
                return

            if not data or "text" not in data:
                self.send_json(400, {"error": "Text required"})
                return

            for note in notes:
                if note["id"] == note_id:
                    note["text"] = data["text"]
                    self.send_json(200, note)
                    return

            self.send_json(404, {"error": "Note not found"})
            return

        self.send_json(404, {"error": "Route not found"})

    # ---------- DELETE Requests ----------
    def do_DELETE(self):
        if not self.rate_limit():
            return

        parts = self.path.strip("/").split("/")

        # ---------- Task 6: Delete Note ----------
        # DELETE /notes/{id}
        if len(parts) == 2 and parts[0] == "notes":
            if not parts[1].isdigit():
                self.send_json(400, {"error": "Invalid ID"})
                return

            note_id = int(parts[1])

            for i, note in enumerate(notes):
                if note["id"] == note_id:
                    notes.pop(i)
                    self.send_response(204)
                    self.end_headers()
                    return

            self.send_json(404, {"error": "Note not found"})
            return

        self.send_json(404, {"error": "Route not found"})


# ---------- Run Server ----------
if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), API)
    print(f"Server running at http://{HOST}:{PORT}")
    server.serve_forever()