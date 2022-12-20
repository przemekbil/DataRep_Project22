from flask import Flask, jsonify, abort
import config, lyrics_api, requests, json

app = Flask(__name__, static_url_path='', static_folder='static_pages')

# API key for Musixmathc server
apikey = config.musicMatch["apiKey"]


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('project.html')

# Return list of artist mathcing the key word
@app.route('/api/find.artist/<name>', methods=['GET'])
def searchTrack(name):

    musix_api_call = "{}{}{}{}{}&apikey={}".format(lyrics_api.base_url, lyrics_api.artist_search, lyrics_api.format_url, lyrics_api.p1, name, apikey)

    response = requests.get(musix_api_call)
    data = response.json()

    artists = []

    # Build a list of dictionary objects with Artist ID and Artist Name only
    for artist in data["message"]["body"]["artist_list"]:
        artists.append({"id":artist["artist"]["artist_id"], "Artist Name":artist["artist"]["artist_name"]})

    return jsonify(artists)

if __name__=="__main__":
    app.run(debug=True)