Basic program that finds the current song playing on my Spotify account and then uses web scraping to display the lyrics.
Requires the Spotipy python module, which can be found here: https://github.com/plamere/spotipy. Public and private 
SPOTIPY_CLIENT_ID's can be created at https://developer.spotify.com/ by creating a project and setting its Redirect URI (found 
in the 'edit settings tab') to your redirect URI. In this case, you would need to set it to http://localhost:8080/callback/. 
In order to verify your client credentials, you need to run a program (I used a basic socket server) at the Spotipy redirect 
URI. in this case, http://localhost:8080/. Also, in order for Spotipy to work properly it CANNOT BE INSTALLED VIA PIP or the 
client.py file has to be reconfigured. 
