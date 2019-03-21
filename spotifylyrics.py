#!/usr/bin/env python3
import os
import requests
from bs4 import BeautifulSoup
import json
import time
import spotify_token as st
import ast
from datetime import datetime

class Spotify:
    def __init__(self, user, passw):
        self.token = None
        self.token_exp = None
        self.user = user
        self.passw = passw
        self.gettoken()
        self.spotheaders = {'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
            }
        self.lyricheaders = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
        self.artist = None
        self.song = None
        self.query = None
        self.lyrics = None
    def gettoken(self):
        if self.token is None or self.token_exp < datetime.now():
            data = st.start_session(self.user, self.passw)
            self.token = data[0]
            self.token_exp = data[1]
    def getsong(self):
        response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=self.spotheaders)
        if response.status_code != 200:
            print(response.status_code)
            print("Bad Response from Spotify API")    
        else:
            json_data = json.loads(response.text)
            self.artist = json_data["item"]["artists"][0]["name"]
            if self.song != json_data["item"]["name"]:
                self.song = json_data["item"]["name"]
                self.query = f"{self.song}+{self.artist}+lyrics"
                self.getlyrics()
    def getlyrics(self):
        s = requests.Session()
        url = f'https://www.google.com/search?q={self.query}&ie=utf-8&oe=utf-8'
        r = s.get(url, headers=self.lyricheaders)
        soup = BeautifulSoup(r.text, "html.parser").find_all("span", {"jsname": "YS01Ge"})
        for link in soup:
            self.lyrics = f"{self.lyrics}\n{link.text}"
        print(f"{self.song}\n")
        print(f"{self.lyrics}\n")

user = input("Please enter spotify username")
passw = input("Please enter spotify password")

spt = Spotify(user, passw)
while True:
    try:
        spt.getsong()
        time.sleep(3)
    except KeyboardInterrupt:
        quit() 
    
