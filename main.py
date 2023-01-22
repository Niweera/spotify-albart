from dotenv import load_dotenv, find_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import json
import requests
from PIL import Image
import os

load_dotenv(find_dotenv())

auth_manager = SpotifyClientCredentials()
spotify = spotipy.Spotify(auth_manager=auth_manager)


def get_album_arts(artist_name, start_date, end_date):
    # Get artist ID by name
    artists = spotify.search(artist_name, type="artist", market="US")
    items = artists.get("artists", {}).get("items", None)

    if items and len(items) > 0:
        artist_uri = items[0].get("uri", "")
        print("selected artist", items[0].get("name"))
    else:
        print("No artist with the given name")
        return

    results = spotify.artist_albums(artist_uri, album_type='album,single', limit=50)

    albums = results.get("items")

    while results.get("next", None):
        results = spotify.next(results)
        albums.extend(results['items'])

    print("albums obtained")

    df = pd.DataFrame(albums)
    df["release_date"] = pd.to_datetime(df["release_date"])
    df = df.sort_values(by=['release_date'], ascending=False)
    df = df[["name", "release_date", "images", "album_type"]]
    df["image"] = df["images"].apply(lambda img: img[0].get("url"))
    final_df = df.loc[(df['release_date'] >= start_date) & (df['release_date'] <= end_date)]

    with open("./image_urls.json", "w") as outfile:
        json.dump(final_df["image"].tolist(), outfile)
        print("image URLs saved")


def save_images(path_to_save):
    with open('./image_urls.json', 'r') as openfile:
        image_urls = json.load(openfile)

    for index, url in enumerate(list(set(image_urls[:50]))):
        img = Image.open(requests.get(url, stream=True).raw)
        img.save(f'{path_to_save}/{index}.png')
        print(f"image saved [{index}]")

    if os.path.exists("./image_urls.json"):
        os.remove("./image_urls.json")
        print("temp files deleted")


if __name__ == '__main__':
    get_album_arts("Artist Name", "Start Date", "End Date")
    save_images("/path/to/save")
