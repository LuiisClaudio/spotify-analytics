from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy_api_extract_engine as spse
import spotify_dataframe_functions as sdf


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
scope = "user-library-read" # Add scopes based on what you want to do

print("Spotify Client ID: ", client_id)
print("Spotify Client Secret: ", client_secret)
print("Spotify Redirect URI: ", redirect_uri)
print("\n")

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)



# Initialize the OAuth manager
auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope
)

# Create the Spotify object
sp = spotipy.Spotify(auth_manager=auth_manager)

# 
df = sdf.prepare_spotify_data('dataset_spotify.csv')

# dump to csv
sdf.export_spotify_data(df, 'dataset/dataset_spotify_cleaned.csv')

track_id_values = df['track_id'].head().copy()

## Audio Features for a Track

#spse.test(sp)

# for track_id in track_id_values:
#     spse.get_track_release_date(sp, track_id)

#df_test = sdf.filter_spotify_data(df, 'track_popularity', 75)
#df_test = sdf.filter_spotify_data(df, 'track_genre', 'edm').head(1000)

#Apply the function for each track_id in the DataFrame and create a new column 'release_date' for each track
#df_test['release_date'] = df_test['track_id'].apply(lambda x: spse.get_track_release_date(sp, x))
#print(df_test[['track_id', 'release_date']])

#sdf.export_spotify_data(df_test, 'dataset_spotify_with_release_dates_edm.csv')

#sdf.export_spotify_data(df_test, 'dataset_spotify_with_release_dates.csv')