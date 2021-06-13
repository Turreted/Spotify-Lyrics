from urllib.parse import urlparse
from urllib.parse import parse_qs
import json

from spotifylyrics.config import SECRETS_CACHE


class StateTokenException(Exception):
    def __init__(self, *args):
        super(Exception, self).__init__("State tokens do not match")


def parse_spotify_http_response(raw_http: str):
    """
    Converts the spotify api's raw http response to a dictionary

    Parameters
    _______

    raw_http: str
        the raw http data from the api

    Output
    ______

    get_headers: dict
         a dict of key value pairs from the response
    """

    # parse out http header data from raw request.
    header_data = next(data for data in raw_http.split() if "code" in data)

    parsed_data = urlparse(header_data).query
    get_headers = parse_qs(parsed_data)

    # merge list response into single string
    for k, i in get_headers.items():
        get_headers[k] = "".join(i)

    return get_headers


def read_refresh_token() -> str:
    """
    Reads the refresh token from spotifylyrics/secrets.json.
    If nothing is found, it returns None

    Outputs
    ______

    refresh_token: str
        the token used to retrive a new access and refresh token from
        the spotify API
    """

    with open(SECRETS_CACHE) as f:
        return json.load(f)["token"]


def cache_refresh_token(token: str, encrypt=False):
    """
    Writes the refresh token to spotifylyrics/secrets.json.

    Parameters
    ______
    token: str
    """

    # for reference: https://stackoverflow.com/a/21035861
    with open(SECRETS_CACHE, "r+") as f:
        contents = json.load(f)
        contents["token"] = token
        f.seek(0)
        json.dump(contents, f, indent=4)  # write file to secrets.json
        f.truncate()
