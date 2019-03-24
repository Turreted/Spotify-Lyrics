Basic program that finds the current song playing on your Spotify account and then uses web scraping to display the lyrics

Installing requirments
```
pip install -r requirements.txt
```

Aside from that, it can be cloned and run as is. 
 
Logging in with environment variables
-------------------------------------

If you prefer to log in without explicitly passing your credentials, you can set 
two environment variables, `SPOTIFY_USERNAME` and `SPOTIFY_PASSWORD`. The script
first check for the existence of those environment variables, only asking for your
credentials via the console if they are not found. 

Command Line Arguments
----------------------

Run script with `--log DEBUG`, `--log INFO`, `--log ERROR` to set the logging level. 
Or leave that argument off entirely and only see logs if errors occur. 
 
Credit to richstokes for streamlining the API interaction and JSON parsing

Credit to TheCannings for properly formatting the code
