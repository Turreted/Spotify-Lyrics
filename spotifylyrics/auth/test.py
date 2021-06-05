from .crypto import generate_client_PKCE
from .http import OAuthServer, TCPRequestHandler
import webbrowser


# the unique id for the Spotify application used to read data
CLIENT_ID = "cabed21db9c54f13b906e562bc864c26"
REDIRECT_URI = "http://localhost:8080/callback/"


http = OAuthServer(("127.0.0.1", 8080))

URL, state_token = generate_client_PKCE(CLIENT_ID, REDIRECT_URI)
webbrowser.open_new_tab(URL)

raw_http_data = http.handle_auth().decode("utf-8")
