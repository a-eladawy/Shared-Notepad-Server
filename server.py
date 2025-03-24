from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Type

# File to store the text
TEXT_FILE = "notepad.txt"

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve the HTML page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/get':
            # Serve the saved text
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            try:
                with open(TEXT_FILE, 'r') as file:
                    self.wfile.write(file.read().encode())
            except FileNotFoundError:
                self.wfile.write(b'')  # Return empty text if file doesn't exist

    def do_POST(self):
        if self.path == '/save':
            # Save the text from the request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            with open(TEXT_FILE, 'w') as file:
                file.write(post_data)

            self.send_response(200)
            self.end_headers()

def run(server_class: Type[HTTPServer] = HTTPServer, handler_class: Type[BaseHTTPRequestHandler] = SimpleHTTPRequestHandler, port: int = 8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()