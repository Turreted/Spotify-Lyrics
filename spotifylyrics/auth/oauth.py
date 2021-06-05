import webbrowser

from spotifylyrics.config import REDIRECT_URI
from spotifylyrics.config import CLIENT_ID

from .utils import parse_spotify_http_response
from .utils import StateTokenException
from .crypto import generate_client_PKCE
from .crypto import exchange_for_access_token
from .http import OAuthServer

from pprint import pprint


def perform_authorization_code_flow():
    """
    Performs spotify's Authorization Code Flow to retrive an API token.
    This uses the OAuth 2.0 protocol, which requires user input and consent.

    """

    # create server that runs at the redirect URI. This is used to catch the
    # response sent from the OAuth authentication
    server = OAuthServer(("127.0.0.1", 8080))

    # generate a uri with the required Oauth headers and open it in a webbrowser
    auth_uri, code_verifier, state_token = generate_client_PKCE(CLIENT_ID, REDIRECT_URI)
    webbrowser.open_new_tab(auth_uri)

    # parse the spotify API's http response for the User's token
    raw_http_response = server.handle_auth().decode("utf-8")
    http_headers = parse_spotify_http_response(raw_http_response)

    # verify that state tokens match to prevent CSRF
    if state_token != http_headers["state"]:
        raise StateTokenException

    # exchange code for access token
    exchange_for_access_token(
        CLIENT_ID, REDIRECT_URI, http_headers["code"], code_verifier
    )


perform_authorization_code_flow()