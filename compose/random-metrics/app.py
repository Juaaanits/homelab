from http.server import HTTPServer, BaseHTTPRequestHandler
import random

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            value = random.uniform(0, 100)
            body = f"my_random_metric {value}\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(body.encode())

        elif self.path == "/healthz":
            body = "ok\n"

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(body.encode())

        else:
            self.send_response(404)
            self.end_headers()

HTTPServer(("0.0.0.0", 8000), MetricsHandler).serve_forever()
