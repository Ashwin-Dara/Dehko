import sys
import json
from yt_post_header import *
sys.path.append('../ytmusicapi')
sys.path.append('../headers_auth_private.json')

from ytmusicapi import YTMusic
YTMusic.setup('headers_auth_private.json', headers_raw=header)
# Official Documentation for YouTube Music API
yt_music = YTMusic()

def play_music(link):
    pass

def play_radio(link):
    pass