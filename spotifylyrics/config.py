import os
import pathlib

"""
Defines application constants
"""

# Spotify application constants

# the unique id for the Spotify application used to read data
CLIENT_ID = "cabed21db9c54f13b906e562bc864c26"
REDIRECT_URI = "http://localhost:8080/callback/"


# directory constants
dir_path = os.path.dirname(os.path.realpath(__file__))
project_root = pathlib.Path(dir_path).parent
