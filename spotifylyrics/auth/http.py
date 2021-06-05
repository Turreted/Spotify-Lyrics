import socketserver
import socket


"""
Create a dead-simple TCP / HTTP server to handle the OAuth request.
This is probably terrible in terms of security, but it only runs locally
and nothing important is sent.
"""

# prevent address already in use error
socketserver.TCPServer.allow_reuse_address = True


class TCPRequestHandler(socketserver.StreamRequestHandler):
    """
    Handles http requests used in OAuth
    """

    def handle(self):

        # read raw http data
        msg = self.rfile.readline().strip()

        # write data to parent class
        self.server.http_data = msg
        self.return_ok()

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

    def return_err(self):
        msg = "HTTP/1.0 500".encode("utf-8")
        self.wfile.write(msg)

    def return_ok(self):
        msg = "HTTP/1.0 200 OK\n\n Got it!".encode("utf-8")
        self.wfile.write(msg)


class OAuthServer(socketserver.TCPServer):
    """
    A socketserver.TCPServer with added functionality to handle POST data
    """

    def __init__(self, addr: tuple):
        super(OAuthServer, self).__init__(addr, TCPRequestHandler)
        self.http_data = None  # stores data from most recent http request

    def handle_auth(self):
        self.handle_request()  # handle single request (Blocking)
        self.server_close()  # gracefully kill server
        return self.http_data
