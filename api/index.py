import json
from http.server import BaseHTTPRequestHandler
import urllib.parse

# Load student data from the JSON file
def load_data():
    with open("q-vercel-python.json", "r") as file:
        data = json.load(file)
    return {entry["name"].strip().lower(): entry["marks"] for entry in data}

STUDENT_DATA = load_data()

# Handler class
class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        # Enable CORS for GET requests
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

        # Parse query parameters
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        names = query.get("name", [])

        # Prepare response
        result = {"marks": []}
        for name in names:
            name_cleaned = name.strip().lower()
            if name_cleaned in STUDENT_DATA:
                result["marks"].append(STUDENT_DATA[name_cleaned])

        # Send JSON response
        self.wfile.write(json.dumps(result).encode("utf-8"))
