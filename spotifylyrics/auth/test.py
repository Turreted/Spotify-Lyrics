from urllib import parse
import secrets
import hashlib
import base64
import webbrowser
import socket


# perform Authorization Code Flow with Proof Key for Code Exchange (PKCE)
# TODO: encrypt Spotify token with spotify password

# the code verifier is a secret key generated on my end
code_verifier = secrets.token_urlsafe(100)

# hash with SHA-256 and convert to base64
code_challenge = hashlib.sha256(code_verifier.encode('utf-8'))
code_challenge = base64.urlsafe_b64encode(code_challenge.digest()).decode('utf-8')
code_challenge = code_challenge.strip('=')


# the unique id for the Spotify application used to read data
CLIENT_ID = "cabed21db9c54f13b906e562bc864c26"
REDIRECT_URI = "http://localhost:8080/callback/"


# Define the permissions of the Spotify-Lyrics application.
# With this scope, it is only able to read your recently played tracks
# More details at https://developer.spotify.com/documentation/general/guides/scopes/#user-read-recently-played
scope = "user-read-recently-played"

endpoint = "https://accounts.spotify.com/authorize"

api_info = {
    "response_type": "code",  # the response requested from the Spotify API
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "code_challenge": code_challenge,
    "scope": scope,
    "code_challenge_method": "S256"  # define hashing method as SHA-256
}

url = parse.urlencode(api_info)
url = "?".join([endpoint, url])

webbrowser.open_new_tab(url)



# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
serversocket.bind(('localhost', 8080))
# become a server socket
serversocket.listen(5)

print("listening on localhost:8080")
data = None

while not data:
    # accept connections from outside
    (clientsocket, address) = serversocket.accept()
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server
    data = clientsocket.recv(2048)

    if data:
        print(data)
        clientsocket.sendall(b"Data Received!")
        clientsocket.close()
        break
