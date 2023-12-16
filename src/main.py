from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import pandas as pd

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    '''
    Get an access token from the Spotify API.

    Returns:
    str: The access token.
    '''
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)#
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    ''' 
    Get the authorization header for the Spotify API.

    Parameters:
    token (str): The access token.

    Returns:
    dict: The authorization header.
    '''
    return{"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    '''
    Searches for an artist on Spotify.

    This function uses the Spotify API to search for an artist by name. It returns the first artist found.

    Parameters:
    token (str): The access token for the Spotify API.
    artist_name (str): The name of the artist to search for.

    Returns:
    dict: A dictionary containing the artist's metadata, or None if no artist was found.
    '''
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    if len(json_result) == 0:
        print("No artist found")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    '''
    Get the top tracks by an artist on Spotify.

    Parameters:
    token (str): The access token.
    artist_id (str): The ID of the artist.

    Returns:
    list: The top tracks by the artist.
    '''
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=DE"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result

def get_albums_by_artist(token, artist_id):
    '''
    Get all albums by an artist on Spotify.

    Parameters:
    token (str): The access token.
    artist_id (str): The ID of the artist.

    Returns:
    list: The albums by the artist.
    '''
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['items']
    return json_result

def get_tracks_from_album(token, album_id):
    '''
    Get all tracks from an album on Spotify.

    Parameters:
    token (str): The access token.
    album_id (str): The ID of the album.

    Returns:
    list: The tracks from the album.
    '''
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['items']
    return json_result

def get_all_songs_by_artist(token, artist_id):
    '''
    Get all songs by an artist on Spotify.

    Parameters:
    token (str): The access token.
    artist_id (str): The ID of the artist.

    Returns:
    list: The songs by the artist.
    '''
    albums = get_albums_by_artist(token, artist_id)
    all_songs = []
    for album in albums:
        tracks = get_tracks_from_album(token, album['id'])
        all_songs.extend(tracks)
    return all_songs

def get_track_metadata(token, track_id):
    '''
    Get the metadata for a track on Spotify.

    Parameters:
    token (str): The access token.
    track_id (str): The ID of the track.

    Returns:
    dict: The metadata for the track.
    '''
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    # Holt die 'external_ids' und die Länge des Releases
    metadata = {
        'name': json_result['name'],
        'external_ids': json_result['external_ids'],
        'duration_ms': json_result['duration_ms'],
    }
    return metadata

def get_all_songs_metadata_by_artist(token, artist_id):
    '''
    Get the metadata for all songs by an artist on Spotify.

    Parameters:
    token (str): The access token.
    artist_id (str): The ID of the artist.

    Returns:
    list: A list of dictionaries containing the metadata for each song.
    '''
    songs = get_all_songs_by_artist(token, artist_id)
    all_songs_metadata = []
    for song in songs:
        metadata = get_track_metadata(token, song['id'])
        all_songs_metadata.append(metadata)
    return all_songs_metadata