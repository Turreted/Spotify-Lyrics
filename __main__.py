import requests
from bs4 import BeautifulSoup
import spotipy.util as util
import spotipy
import json
from io import StringIO
import time

query = ''
currentSong = ''
PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID = '<YOUR ID>' # Your SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET can be created at https://developer.spotify.com/
SPOTIPY_CLIENT_SECRET = '<YOUR SECRET KEY>'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080/'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'
URL = 'http://localhost:8080/callback/'
username = '<YOUR USERNAME>'
scope = 'user-read-currently-playing'


def song_data():
    global query
    currentSongData = []
    remove = ['name', "'", '"', '\n', ',', ':', " '", ' Various Artists', 'Remastered Version']
    token = util.prompt_for_user_token(username,scope,client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=URL)
    sp = spotipy.Spotify(auth=token)
    playing = json.dumps(sp.current_user_playing_track(), sort_keys=True, indent=0)
    s = StringIO(str(playing))
    for line in s:
        if 'name' in line:
            for char in remove:
                line = line.replace(char, '')
            if '-' in line:
                line = line[:line.find('-')]
            currentSongData.append(line)
    try:
        query = currentSongData[len(currentSongData) - 1] + ' lyrics'
        display = currentSongData[len(currentSongData) - 1] ' by ' + currentSongData[0]
        return display
    except IndexError:
        return 'Device Disconnected'


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
    soup = BeautifulSoup(r.text, "html.parser")
    soup = soup.find_all("span", {"jsname": "YS01Ge"})
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
        time.sleep(0.5)


if __name__ == '__main__':
    main()
