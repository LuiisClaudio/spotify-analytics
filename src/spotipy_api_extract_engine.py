# shows acoustic features for tracks for the given artist

import json
import time
import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_track_release_date(sp_client, track_id):
    try:
        track = sp_client.track(track_id)
        track_release_date = track['album']['release_date']
        # If the release date is only the year, force the format to year-01-01
        if len(track_release_date) == 4:
            track_release_date = f"{track_release_date}-01-01"
        return track_release_date
    except Exception:
        return None

def get_track_release_date_bkp(sp_client, track_id):
    track = sp_client.track(track_id)
    #print("Track Release Date: ", track['album']['release_date'])
    track_release_date = track['album']['release_date']
    # If the release date is only the year, force the format to year-01-01
    if len(track_release_date) == 4:
        track_release_date = f"{track_release_date}-01-01"
    #print("Track Release Date Review: ", track_release_date)
    return track_release_date
    
def test(sp_client):
    results = sp_client.current_user_saved_tracks()
    #print("Results: ", results)

    for item in results['items']:
        track = item['track']
        #print(f"{track['id']}")
        #print(f"{track['id']}, {track['name']}, {track['album']['name']}, {track['album']['release_date']}, {track['popularity']}, {track['duration_ms']}, {track['track_number']}, {track['type']}, {track['uri']}")
        get_track_release_date(sp_client, track['id'])