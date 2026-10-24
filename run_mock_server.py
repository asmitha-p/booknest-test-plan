"""Serves ./mock_app on http://localhost:8000 and returns a friendly 404 page.

Usage:  python run_mock_server.py [port]
The test suite starts this server automatically (see tests/conftest.py), so
running it by hand is only needed for manual exploration.
"""
import functools
import sys
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

APP_DIR = Path(__file__).parent / "mock_app"


class AppHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):  # keep test output clean
        pass

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            body = (APP_DIR / "404.html").read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().send_error(code, message, explain)


def make_server(port: int = 8000) -> HTTPServer:
    handler = functools.partial(AppHandler, directory=str(APP_DIR))
    return HTTPServer(("localhost", port), handler)


def start_in_background(port: int = 8000) -> HTTPServer:
    server = make_server(port)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"Mock app running at http://localhost:{p}/login.html (Ctrl+C to stop)")
    make_server(p).serve_forever()
