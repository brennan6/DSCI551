import json
import requests

FIREBASE_URL = "https://project-dsci551.firebaseio.com/songs.json"

with open('pyspark_output.json') as json_file:
    results = json.load(json_file)

def send_json_to_firebase(dict_songs, url):
    """ (4) Send the data to the firebase url for import by Front End. """
    json_songs = json.dumps(dict_songs)
    r = requests.put(url, json_songs)
    return

send_json_to_firebase(results, FIREBASE_URL)
