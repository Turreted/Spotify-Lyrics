from secrets import token_urlsafe
from hashlib import sha256
from base64 import urlsafe_b64encode
from urllib import parse

import requests

"""
This file contains all methods used for Spotify's OAuth handshake and token renewal.
"""


def generate_client_PKCE(
    client_id: str,
    redirect_uri: str,
    scopes="user-read-recently-played",
    verifier_entropy=64,
    state_entropy=16,
):

    """
    Method to generate the URL Spotify's Authorization Code Flow
    with Proof Key for Code Exchange (PKCE). With the default
    scope, this allows the application to view the songs you
    have most recently listened to.

    This program flow is used when the user does not want to enable
    token caching, as the tokens it grants only last a short time.

    More information can be found in the Spotify docs:
    https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow-with-proof-key-for-code-exchange-pkce

    Parameters
    _________

    client_id: str
        The client id for the spotify application that is
        being authenticated. 

    redirect_uri: str
        The URI that the program redirects to after authentication.

    scopes: str (List of space-seperated scopes)
        These define the permissions of the Spotify-Lyrics application.
        The default is "user-read-recently-played." With this scope, the app
        is only able to read your recently played tracks. More details at:
        https://developer.spotify.com/documentation/general/guides/scopes/#user-read-recently-played

        Note that if you need to add an additional scope, you may add it as
        part of a space-seperated list.

    verifier_entropy: int
        the bits of entropy used in the code_verifier (the client secret key).
        Note that this must be between 43 and 128 chars in length.

    state_entropy: int
        the bits of entropy used in the state token.


    Output
    ______

    OAuth_url: str
        the URL the client must navigate to in order to perform OAuth verification.

    state_token: str
        a token used to prevent CSRF.The data returned by the spotify API should
        match this token. Read more here: https://auth0.com/docs/protocols/state-parameters

    code_verifier: str
        the secret key identifier, which is used to authenticate the program later
    """

    # define the spotify API auth endpoint
    endpoint = "https://accounts.spotify.com/authorize"

    # Generate the code_verifier, which is my secret identifier
    code_verifier = urlsafe_b64encode(token_urlsafe(verifier_entropy).encode("utf-8"))
    code_verifier = code_verifier.strip(b"=")

    # hash with SHA-256 and convert to base64 to encrypt secret.
    code_challenge = urlsafe_b64encode(sha256(code_verifier).digest())
    code_challenge = code_challenge.decode("utf-8").strip("=")

    # generate state token to prevent CSRF
    state_token = token_urlsafe(state_entropy)

    # construct the POST request data with the parameters specified in the Spotify Docs
    api_headers = {
        "response_type": "code",  # the response requested from the Spotify API
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code_challenge": code_challenge,
        "scope": scopes,
        "code_challenge_method": "S256",  # define hashing method as SHA-256
        "state": state_token,
    }

    # create the endpoint url with all required data
    payload = parse.urlencode(api_headers)
    OAuth_url = "?".join([endpoint, payload])

    return OAuth_url, code_verifier, state_token


def exchange_for_access_token(
    client_id: str, redirect_uri: str, auth_code: str, code_verifier: str
):
    """
    Exchanges the code retrived in the OAuth authentication for a spotify API key and refresh token.

    More information can be found in the Spotify docs:
    https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow-with-proof-key-for-code-exchange-pkce


    Parameters
    __________

    auth_code: str
        the code retrived from the Spotify API in the OAuth flow

    client_id: str
        The client id for the spotify application that is being authenticated.

    redirect_uri: str
        The URI that the previous step redirected to after authentication.

    code_verifier: str
        the secret key generated in the previous step of this program

    Output
    ______

    api_key: str
        a user's api key with prompted permissions

    refresh_token: str
        A refresh token used to retrive future api keys
    """

    # Spotify's token exchange endpoint
    endpoint = "https://accounts.spotify.com/api/token"

    api_headers = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code": auth_code,
        "code_verifier": code_verifier,
        "grant_type": "authorization_code",
    }

    r = requests.post(endpoint, data=api_headers)
    print(r.text)
