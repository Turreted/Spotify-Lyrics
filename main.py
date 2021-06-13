#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from spotifylyrics.api import SpotifyApi


def main():
    spotify_listener = SpotifyApi()
    spotify_listener.serve_forever()


if __name__ == "__main__":
    main()
