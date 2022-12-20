from flask import Flask, jsonify, abort
import config, lyrics_api, requests, json

app = Flask(__name__, static_url_path='', static_folder='static_pages')

# API key for Musixmathc server
apikey = config.musicMatch["apiKey"]


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('project.html')

# Return list of artists albums 
@app.route('/api/mm/show.artist.albums/<artist_id>', methods=['GET'])
def findAlbum(artist_id):

    musix_api_call = "{}{}{}{}{}&apikey={}".format(lyrics_api.base_url, lyrics_api.artist_album_getter, lyrics_api.format_url, lyrics_api.p4, artist_id, apikey)

    response = requests.get(musix_api_call)
    data = response.json()

    albums =[]

    for album in data["message"]["body"]["album_list"]:
        albums.append({
            "album_id":album["album"]["album_id"],
            "album_name":album["album"]["album_name"],
            "album_release_date": album["album"]["album_release_date"],
            "album_label": album["album"]["album_label"]
        })
    
    return jsonify(albums)

# Return list of artist matching the key word
@app.route('/api/mm/find.artist/<name>', methods=['GET'])
def searchTrack(name):

    musix_api_call = "{}{}{}{}{}&apikey={}".format(lyrics_api.base_url, lyrics_api.artist_search, lyrics_api.format_url, lyrics_api.p1, name, apikey)

    response = requests.get(musix_api_call)
    data = response.json()

    artists = []

    # Build a list of dictionary objects with Artist ID and Artist Name only
    for artist in data["message"]["body"]["artist_list"]:
        artists.append({
            "artist_id":artist["artist"]["artist_id"],
            "artist_Name":artist["artist"]["artist_name"]
            })

    return jsonify(artists)

if __name__=="__main__":
    app.run(debug=True)