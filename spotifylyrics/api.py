#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Purpose of File is defined here
"""

import getpass
import json
import time

from datetime import datetime

import requests
from bs4 import BeautifulSoup
import spotify_token as st

from utils import init_argparser
from utils import init_logger


argparser = init_argparser()
args = argparser.parse_args()
logger = init_logger(args.log)


class SpotifyApi:

    def __init__(self, user, passw, **kwargs):
        self.token = None
        self.token_exp = None
        self.user = user
        self.passw = passw
        self.get_token()

        # The headers for the GET request sent to the Spotify API in order to
        # retrieve the current song
        self.spotheaders = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        # The headers for the Google search used to find the song lyrics
        self.lyricheaders = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

        # spotify data stored in class variables
        self.artist = None
        self.song = None
        self.query = None
        self.lyrics = ""

    def create_token(self):
        pass

    def refresh_token(self):
        """
        Gets the user's api token via Spotify's XXXXXXXX
        """
        logger.info("getting token")

        # if our api token is nonexistent or expired, get a new one
        if not self.token or self.token_exp < datetime.now():

            logger.info("no token found, starting new session")

            logger.info("token acquired")

        else:
            logger.info("using cached token")


    def get_cur_song(self):
        """
        Submits a GET request to the Spotify API with the valid OAuth token
        which returns a JSON object containing the song + artist
        playing on the user's account
        """

        logger.debug("calling `getsong`")
        response = requests.get(
            "https://api.spotify.com/v1/me/player/currently-playing",
            headers=self.spotheaders,
        )

        logger.debug(f"status code: {response.status_code}")

        try:
            if response.status_code == 204:
                logger.info("No song playing")
            if not response.json():
                logger.debug("no json payload")
                return

        except requests.exceptions.HTTPError as e:
            raise e

        else:
            json_data = json.loads(response.text)
            # parses the JSON object returned by the Spotify API and uses it to define self.song and self.artist
            currently_playing = json_data.get("currently_playing_type")
            if not currently_playing.lower() == "track":
                return currently_playing
            self.artist = json_data["item"]["artists"][0]["name"]
            if self.song != json_data["item"]["name"]:
                self.song = json_data["item"]["name"]

                # Constructs a google query out of self.song and self.artist
                self.query = (
                    str(self.song) + "+" + str(self.artist) + "+lyrics"
                ).replace(" ", "+")
                self.getlyrics()
                return self.song

    def get_lyrics(self):
        pass


def main(*args):
    """
    username, password = os.getenv("SPOTIFY_USERNAME"), os.getenv("SPOTIFY_PASSWORD")
    if not (username and password):
        username = input("Spotify Username: ")
        password = getpass.getpass()
    """

    spt = SpotifyApi("gideonmitchell", "Plutonium94")
    last = None

    """
    while True:
        try:
            current = spt.getsong()
            if current != last and current:
                print(f"Currently Playing: {current}")
                last = current
            time.sleep(3)
        except KeyboardInterrupt:
            quit()
        except Exception:
            logger.exception("Error occured", exc_info=True)
    """

if __name__ == "__main__":
    main()
