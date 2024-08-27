from flask import Flask, render_template
import os
import requests
import random

app = Flask(__name__)

# Genius API configuration
GENIUS_API_URL = "https://api.genius.com/search?q=Beyonc%C3%A9"
HEADERS = {
    "Authorization": "Bearer SFzda4l4Fl_TGiduQU5qeS0La4z5_xfnAEqMLXy_OVZMn3BdbXgy4ACESFxlnTcJ"
}

def get_songs():
    try:
        response = requests.get(GENIUS_API_URL, headers=HEADERS)
        response.raise_for_status()
        json_body = response.json()
        if 'response' in json_body and 'hits' in json_body['response'] and len(json_body['response']['hits']) > 0:
            songs = json_body['response']['hits']
            song_list = []
            for song in songs:
                song_list.append({
                    'title': song['result']['full_title'],
                    'song_art_image_url': song['result']['song_art_image_url'],
                    'artist_name': song['result']['primary_artist']['name'],
                    'url': song['result']['url']
                })
            return song_list
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching songs: {e}")
        return []

@app.route('/')
def index():
    songs = get_songs()
    # Shuffle the songs for variety
    random.shuffle(songs)
    return render_template('index.html', songs=songs)


if __name__ == '__main__':
    app.run(
        port=int(os.getenv('PORT', 8080)),
        host=os.getenv('IP', '0.0.0.0'),
        debug=True
    )

