from urllib.parse import urlparse, parse_qs


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
    header_data = next(data for data in raw_http.split() if "?code=" in data)

    parsed_data = urlparse(header_data).query
    get_headers = parse_qs(parsed_data)

    # merge list response into single string
    for k, i in get_headers.items():
        get_headers[k] = "".join(i)

    return get_headers
