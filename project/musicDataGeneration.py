import lyricsgenius as lg
import requests, json
from time import sleep
from PIL import Image
import requests
from io import BytesIO

ACCESS_TOKEN = ""
genius = lg.Genius(ACCESS_TOKEN, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)

FIREBASE_URL = "https://project-dsci551.firebaseio.com/songs.json"
artists = ["Morgan Wallen", "Sam Hunt", "Luke Bryan", "Taylor Swift", "Old Dominion", "Kenny Chesney", "Jon Pardi", "Luke Combs", "George Strait", "Kacey Musgraves",
           "Shawn Mendes", "Maggie Rogers", "Florida Georgia Line", "Toby Keith", "Dierks Bentley", "Kip Moore", "Tim McGraw", "Zac Brown Band", "Jake Owen", "Thomas Rhett"]

def get_lyrics(artist_arr, num):
    """ Uploads the data needed for the project to firebase after scraping from Genius API """
    artists_dict = {}
    artists_dict["songs"] = []
    for name in artist_arr:
        try:
            songs = genius.search_artist(name, max_songs=num, sort='popularity').songs
            for song in songs:
                img_response = requests.get(song.song_art_image_url)
                img = Image.open(BytesIO(img_response.content))
                rgb_scores = [tup[2] for tup in img]
                artists_dict['songs'].append({
                    'title': song.title,
                    'artist': name,
                    'album': song.album,
                    'year': song.year,
                    'featured_artists': song.featured_artists,
                    'writer_artists': song.writer_artists,
                    'image_url': song.song_art_image_url,
                    'image_height': img.size[0],
                    'imgage_width': img.size[1],
                    'lyrics': song.lyrics
                })
        except Exception as e:
            raise(e)
    return artists_dict

def send_json_to_firebase(dict_songs, url):
    json_songs = json.dumps(dict_songs, cls=NumpyArrayEncoder)
    r = requests.put(url, json_songs)
    return

artists_dict = get_lyrics(artists, 10)
send_json_to_firebase(artists_dict, FIREBASE_URL)
