#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import time

query = ''
currentSong = ''
TOKEN = ''
# Get oauth token from https://developer.spotify.com/console/get-users-currently-playing-track

def song_data():
    global query
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + TOKEN,
    }

    response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    json_data = json.loads(response.text)
    try:
        ARTIST = json_data["item"]["artists"][0]["name"]
        SONG = json_data["item"]["name"]
        query = SONG + " " + ARTIST + " +lyrics"
        return 'Artist: %s, Song: %s' % (ARTIST, SONG)
    except KeyError:
        return currentSong



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
    global query
    print(song_data())
    currentSong = song_data()
    print(get_Song_Lyrics(query))
    while True:
        if song_data() != currentSong:
            print(song_data())
            print(get_Song_Lyrics(query))
            currentSong = song_data()
        time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Quitting..')
        try:
            quit()
        except SystemExit:
            quit()
