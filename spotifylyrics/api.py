#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import time

import schedule
import requests
import colorama

from bs4 import BeautifulSoup

from spotifylyrics.auth.utils import read_refresh_token
from spotifylyrics.auth.crypto import exchange_refresh_token
from spotifylyrics.auth.oauth import perform_authorization_code_flow


# start colorama
colorama.init()


class SpotifyApi:

    # the HTML tags containing all lyric data on google
    lyric_container_scopes = {"jsname": "YS01Ge"}

    def __init__(self, clear=True, **kwargs):
        self.current_song = None
        self.clear_screen = clear

        # track the access and refresh tokens, used to access the user's spotify data
        self.access_token = None
        self.refresh_token = read_refresh_token()

        # if we have a cached refresh token, use it instead of OAuth
        if self.refresh_token:
            self.__exchange_refresh_token()

        # Otherwise, we must perfrom OAuth exchange, which requires prompting the user.
        # This is done with Spotify's client PKCE auth flow
        else:
            (
                self.access_token,
                self.refresh_token,
                token_duration,
            ) = perform_authorization_code_flow()

            # tracks the time until the token expires
            self.expires_at = time.time() + token_duration

        # run and update song info
        self.__update_song_info()

    def __exchange_refresh_token(self):
        """
        Exchanges the current refresh token for a new API key and refresh token.
        Used when the current API key is unknown or expired.
        """

        self.access_token, self.refresh_token, token_duration = exchange_refresh_token(
            self.refresh_token
        )

        self.expires_at = time.time() + token_duration

    def __get_song_metadata(self) -> dict:
        """
        Gets the api data for the song that the user is currently playing.

        Output
        ______
            api_data: json object
                A json object containing the data from the API endpoint
        """

        endpoint = "https://api.spotify.com/v1/me/player/currently-playing"

        api_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

        resp = requests.get(endpoint, headers=api_headers)
        return resp.json() if resp.text else None

    def __get_current_song(self) -> tuple:
        """
        Gets the title and artist of the song currently playing on the user's spotify account.
        If no song is currently playing, return None.

        Outputs
        _______

            song: str
                The song that is currently being played

            artist: str
                The artist of the current song
        """

        song_metadata = self.__get_song_metadata()
        song_title, artist = None, None

        # pass if API result is malformed (for example, if an ad is playing)
        try:
            song_title, artist = (
                song_metadata["item"]["name"],
                song_metadata["item"]["artists"][0]["name"],
            )
        except (TypeError, KeyError):
            pass

        return (song_title, artist) if song_metadata else (None, None)

    def __get_lyrics(self, song_title: str, artist: str) -> str:
        """
        Scrapes Google lyrics for the lyrics of the song currently playing.
        This is done by imitating a google search and using BeautifulSoup to
        scrape HTML elements from the result. It's very hacky, but it still works
        after two years so I'm keeping it.

        Parameters
        __________

            song_title: str
                The title of the song that is being scraped (e.g "Dark Star")

            artist: str
                The name of the artist of the scraped song (e.g "The Grateful Dead")


        Output
        ______

            lyrics: str
                a string lf song lyrics with newlines
        """

        endpoint = "http://www.google.com/search?q={}"

        # remove everything after these characters in a song title, as it makes the program less accurate
        song_str_terminators = ["-", ";", ":", "(", "["]

        for char in [c for c in song_str_terminators if c in song_title]:
            song_title = song_title[0 : song_title.find(char)]

        # parse into URL format. Ripped straight from https://stackoverflow.com/a/1007615
        google_query = " ".join([song_title, "by", artist, "lyrics"])
        google_query = re.sub(r"[^\w\s]", "", google_query)
        google_query = re.sub(
            r"\s+", "+", google_query
        )  # Replace all runs of whitespace with a single '+'

        # Webbrowser-imitation header is required to make google think we're human
        google_headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        }

        # construct query and make request
        query_url = endpoint.format(google_query)
        request_body = requests.get(query_url, headers=google_headers)

        # parse out HTML elements with song lyrics
        soup = BeautifulSoup(request_body.text, "html.parser").find_all(
            "span", self.lyric_container_scopes
        )

        # output lyrics
        return "\n".join([tag.text for tag in soup])

    def __pretty_print(self, song_title: str, artist: str, lyrics: str):
        """
        prints out the song title, artist, and lyrics
        """

        # clear the screen
        if self.clear_screen:
            [os.system("cls") if os.name == "nt" else print("\033c", end="")]

        song_header = song_title + " by " + artist
        print(colorama.Fore.GREEN + song_header)
        print(colorama.Style.DIM + ("-" * len(song_header)))
        print(colorama.Style.RESET_ALL)

        if lyrics:
            print(lyrics + "\n")

    def __check_token_expiration(self):
        """
        Checks if the current API token has expired. if so, it is refreshed.
        """

        # refresh the token a minute before expiration so there are no errors.
        if time.time() + 60 > self.expires_at:
            self.__exchange_refresh_token()

    def __update_song_info(self):
        """
        Checks if the user has chenged songs. If the song has changed,
        then the lyrics of the new song are printed to the terminal.
        This can be considered the core function of the class.
        """

        song, artist = self.__get_current_song()

        # check if user has switched songs
        if song != self.current_song and song:
            self.current_song = song

            # get and print lyrics to new song
            lyrics = self.__get_lyrics(song, artist)
            self.__pretty_print(song, artist, lyrics)

    def serve_forever(self, interval: int = 10):
        """
        Checks every {interval} seconds if the user's song has changed or the token has expired on a permanent
        loop. This is the only public method in the class, and should be called after the constructor.

        Parameters
        _________

            interval: int
                The duration between requests. For example, if the interval is 10, then
                the program will wait 10 seconds before checking if the song has changed.
        """

        schedule.every(interval).seconds.do(self.__check_token_expiration)
        schedule.every(interval).seconds.do(self.__update_song_info)

        while True:
            schedule.run_pending()
            time.sleep(1)
