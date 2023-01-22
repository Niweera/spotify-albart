# Spotify-AlbArt

Spotify-AlbArt is used to get Album Arts from Spotify for a given artist.

## How to run

[Get](https://developer.spotify.com/) Spotify Client ID and Client Secret and add in the `.env` file.

```dotenv
SPOTIPY_CLIENT_ID='SPOTIPY_CLIENT_ID'
SPOTIPY_CLIENT_SECRET='SPOTIPY_CLIENT_SECRET'
```

Update params in `./main.py`

```python
if __name__ == '__main__':
    get_album_arts("Artist Name", "Start Date", "End Date")
    save_images("/path/to/save")

# Start Date "2022-01-01"
# End Date "2022-12-31"
```

```bash
<venv> $ pip install -r requirements.txt
<venv> $ python main.py
```

#### This program uses [spotipy](https://spotipy.readthedocs.io/en/latest/).
