Basic program that finds the current song playing on your Spotify account and then uses web scraping to display the lyrics

Installing requirements
----------------------
All requirements can be installed with
```
pip install -r requirements.txt
```

Logging in with environment variables
-------------------------------------

If you prefer to log in without explicitly passing your credentials, you can set
two environment variables, `SPOTIFY_USERNAME` and `SPOTIFY_PASSWORD`. The script
first check for the existence of those environment variables, only asking for your
credentials via the console if they are not found.

```
# ~/.bash_profile
...
export SPOTIFY_USERNAME=your_username
export SPOTIFY_PASSWORD=your_password
...
```

Security and Privacy
--------------------

Due to recent changes in Spotify's API policies 

Command Line Arguments
----------------------

Run script with `--log DEBUG`, `--log INFO`, `--log ERROR` to set the logging level. 
Or leave that argument off entirely and only see logs if errors occur. 

Collaborators
-------------
Credit to richstokes for streamlining the API interaction and JSON parsing

Credit to TheCannings for properly formatting the code

Credit to AirbusDriver for adding the parser, get_credentials(), and the debugging system
