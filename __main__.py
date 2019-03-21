#!/usr/bin/env python3
import os
import requests
from bs4 import BeautifulSoup
import json
import time
import spotify_token as st
import ast

USER = ''
PW = ''
query = ''
currentSong = ''
TOKEN = ''
dirname, filename = os.path.split(os.path.abspath(__file__))
os.chdir(dirname)

try:
    with open("Cached_Data.txt","w") as file:
        file.close()
except:
    pass

cache = open('Cached_Data.txt', 'r+')
if os.stat("Cached_Data.txt").st_size == 0 and cache.readline() != '\n':
    cache.truncate(0)
    USER = input('Spotify Username: ')
    PW = input('Spotify Password: ')
    cache.write("['{}', '{}']".format(USER, PW))
else:
    data = ast.literal_eval(str(cache.readline()))
    USER = data[0]
    PW = data[1]


def get_token():
    global TOKEN
    data = st.start_session(USER,PW)
    TOKEN = data[0]
    expiration_date = data[1]


def song_data():
    global query
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + TOKEN,
    }

    try:
        response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
        json_data = json.loads(response.text)
        ARTIST = json_data["item"]["artists"][0]["name"]
        SONG = json_data["item"]["name"]
    except:
        print('JSON Response Error.')  # TODO handle this better
        get_token()  # Hacky, but fair to assume if API is not responding it could be due to an expired token
        # print(response.content)
        return currentSong
    finally:
        query = SONG + " " + ARTIST + " +lyrics"
        return('Artist: %s, Song: %s' % (ARTIST, SONG))


headers_Get = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }


def get_Song_Lyrics(query):
    minestrone = '\n'
    s = requests.Session()
    query = '+'.join(query.split())
    url = 'https://www.google.com/search?q=' + query + '&ie=utf-8&oe=utf-8'
    r = s.get(url, headers=headers_Get)
    soup = BeautifulSoup(r.text, "html.parser").find_all("span", {"jsname": "YS01Ge"})
    for link in soup:
        minestrone += (link.text + '\n')
    return minestrone


def main():
    get_token()
    global query
    print(song_data())
    currentSong = song_data()
    print(get_Song_Lyrics(query))
    while True:
        if song_data() != currentSong:
            print(song_data())
            print(get_Song_Lyrics(query))
            currentSong = song_data()
        time.sleep(3)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Quitting..')
        try:
            quit()
        except SystemExit:
            quit()
