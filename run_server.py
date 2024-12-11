#!/usr/bin/env python3
"""
Enhanced HTTP server with structured logging.
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import logging
from urllib.parse import parse_qs
import re


def setup_logging():
    """
    Configure logging to separate access logs and error logs.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("access.log"),
            logging.StreamHandler()
        ]
    )

    error_handler = logging.FileHandler("error.log")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logging.getLogger().addHandler(error_handler)

def safeget(dct, *keys):
    """
    Safely retrieves a nested value from a dictionary using the provided keys.
    Returns None if any key is missing.
    """
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
    return dct

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler with enhanced logging.
    """

    def _set_response(self, code=200, content_type='text/html'):
        """
        Sets the HTTP response headers.
        """
        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def log_request_details(self):
        """
        Logs details of the incoming request.
        """
        logging.info(
            "Processing request: Method=%s, Path=%s, Headers=%s",
            self.command, self.path, self.headers
        )

    def do_post(self):  # noqa: C0103
        """
        Handles POST requests with detailed logging.
        """
        self.log_request_details()
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_data_fields = parse_qs(post_data)

            logging.debug("POST data received: %s", post_data_fields)

            self._set_response()

            if (re.match("^/register", self.path) and
                safeget(post_data_fields, "username", 0) == "admin@domain.com" and
                safeget(post_data_fields, "password", 0) == "rainbow"):
                response = "<h1>Congrats, you succeeded to submit the correct data</h1>"
                logging.info("Successful registration for user admin@domain.com")
            else:
                response = f"""
                    <h1>Error: Bad Request</h1>
                    POST request for {self.path}<br>Body: {post_data}
                """
                logging.warning("Failed registration attempt for path: %s", self.path)

            self.wfile.write(response.encode('utf-8'))

        except ImportError as e:  # noqa: W0718
            logging.error("POST request failed: %s", str(e), exc_info=True)
            self._set_response(500)
            self.wfile.write(b"Internal Server Error")

def run(server_class=HTTPServer, handler_class=CustomHTTPRequestHandler,
 server_port=8000):  # port -> server_port
    """
    Starts the HTTP server.
    """
    setup_logging()
    server_address = ('', server_port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting HTTP server on port %d", server_port)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down the server.")
        httpd.server_close()

if __name__ == '__main__':
    from sys import argv

    PORT = int(argv[1]) if len(argv) == 2 else 8000  # port -> PORT
    run(server_port=PORT)
