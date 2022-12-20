from flask import Flask, jsonify, abort
import config, lyrics_api, requests, json

app = Flask(__name__, static_url_path='', static_folder='static_pages')

# API key for Musixmathc server
apikey = config.musicMatch["apiKey"]


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('project.html')


@app.route('/api/find.artist/<name>', methods=['GET'])
def searchTrack(name):

    api_call = "{}{}{}{}{}&apikey={}".format(lyrics_api.base_url, lyrics_api.artist_search, lyrics_api.format_url, lyrics_api.p1, name, apikey)
    print(api_call)

    response = requests.get(api_call)
    data = response.json()

    output = json.dumps(data, sort_keys=True, indent=2)

    #for artist in data["message"]["body"]["artist_list"]:
    #    print("id:{}, {}".format(artist["artist"]["artist_id"], artist["artist"]["artist_name"]))


    #return app.send_static_file('searchTrack.html')
    return output

if __name__=="__main__":
    app.run(debug=True)