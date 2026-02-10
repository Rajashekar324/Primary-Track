from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

HOST = "localhost"
PORT = 8000


class ProductAPI(BaseHTTPRequestHandler):

    def send_json(self, status=200, data=None):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if data is not None:
            self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path != "/products":
            self.send_json(404, {"error": "Route not found"})
            return

        params = parse_qs(parsed_url.query)

        # Query params (strings!)
        name = params.get("name", [""])[0].lower()
        max_price = params.get("max_price", [None])[0]

        if max_price is not None:
            max_price = int(max_price)

        # Sample product data
        products = [
            {"id": 1, "name": "Phone", "price": 400},
            {"id": 2, "name": "Laptop", "price": 800},
            {"id": 3, "name": "Headphone", "price": 150},
            {"id": 4, "name": "Smartphone", "price": 600},
            {"id": 5, "name": "Phone Case", "price": 50},
        ]

        # 🔍 Filter logic
        results = []

        for p in products:
            if name and name not in p["name"].lower():
                continue
            if max_price is not None and p["price"] > max_price:
                continue
            results.append(p)

        self.send_json(200, results)


def run():
    server = HTTPServer((HOST, PORT), ProductAPI)
    print(f"Server running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run()