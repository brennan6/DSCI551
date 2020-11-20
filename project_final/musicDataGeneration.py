import lyricsgenius as lg
import requests, json
from time import sleep
from PIL import Image
import requests
from io import BytesIO

ACCESS_TOKEN = "8XYfdF4UbEnItXc5gdcPHIA9WGXo9gOfNeLOswUhg-vtBZsKOxdp2_P3r8KD36Lc"
genius = lg.Genius(ACCESS_TOKEN, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)

artists = ["Morgan Wallen", "Sam Hunt","Luke Bryan", "Taylor Swift", "Old Dominion", "Kenny Chesney", "Jon Pardi", "Luke Combs", "George Strait", "Kacey Musgraves",
        "Shawn Mendes", "Maggie Rogers", "Florida Georgia Line", "Toby Keith", "Dierks Bentley", "Kip Moore", "Tim McGraw", "Zac Brown Band", "Jake Owen", "Thomas Rhett"]

def get_lyrics(artist_arr, num):
    """ (1) Scrape the song data from Genius API. Output - artist_data.json """
    artists_dict = {}
    artists_dict["songs"] = []
    for name in artist_arr:
        print("Name to Search:", name)
        try:
            songs = genius.search_artist(name, max_songs=num, sort='popularity').songs
            for song in songs:
                img_response = requests.get(song.song_art_image_url)
                img = Image.open(BytesIO(img_response.content))
                artists_dict['songs'].append({
                    'title': song.title,
                    'artist': name,
                    'album': song.album,
                    'year': song.year,
                    'featured_artists': song.featured_artists,
                    'writer_artists': song.writer_artists,
                    'image_url': song.song_art_image_url,
                    'image_height': img.size[0],
                    'image_width': img.size[1],
                    'lyrics': song.lyrics
                })
        except Exception as e:
            raise(e)
    return artists_dict

def write_json_file(dict_songs):
    with open('artist_data.json', 'w') as outfile:
        json.dump(dict_songs["songs"], outfile)

artists_dict = get_lyrics(artists, 10)
write_json_file(artists_dict)