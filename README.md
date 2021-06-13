# Spotify Lyrics 🎵

A dead-simple program to find lyrics for your favorite songs - just run ./main.py and have the lyrics for whatever you're playing on Spotify displayed to your terminal

Installing requirements
----------------------
All requirements can be installed with
```
pip install -r requirements.txt
```

Security and Privacy
--------------------

Due to recent changes in Spotify's API policies, you now must authenticate the application
via OAuth 2.0. Once this is done, Spoify-Lyrics will cache your Spotify refresh token in
```spotifylyrics/cache/secrets/json```.

If this token is stolen, the only thing that the attacker would be able to do with it is
know what songs you're currently listening to. If you need to, you can always revoke access
by going to https://www.spotify.com/us/account/apps/ and click "Remove Access" for the app "Lyric-Streaming"


Collaborators
-------------
- Thank You to richstokes for streamlining the API interaction and JSON parsing
- Thank You to TheCannings for properly formatting the code
- Thank You to AirbusDriver for adding the parser, get_credentials(), and the debugging system
