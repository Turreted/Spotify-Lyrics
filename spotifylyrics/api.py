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

    def __init__(self, **kwargs):
       pass

    def create_token(self):
        pass

    def refresh_token(self):
        pass

    def get_cur_song(self):
        pass

    def get_lyrics(self):
        pass
