from flask import Flask, jsonify, request, abort
import config, lyrics_api, requests, json
from projectDAO import userDAO, favoritesDAO

app = Flask(__name__, static_url_path='', static_folder='static_pages')

# API key for Musixmathc server
apikey = config.musicMatch["apiKey"]


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('project.html')

# Return list of registered profiles
@app.route('/api/users', methods=['GET'])
def getUsers():

    users = userDAO.getAll()
    return jsonify(users)


@app.route('/api/user/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def api_user(user_id):
    user = userDAO.findByID(user_id)

    if user is None:
        return 'User not found', 404
    if request.method == 'GET':
        # Return the user
        return jsonify(user)
    elif request.method == 'PUT':
        # Update the user
        data = request.get_json()
        user.name = data['name']
        userDAO.update(user.name, user.user_id)

        user = userDAO.findByID(user_id)
        return jsonify({'id': user.user_id, 'name': user.name})
    elif request.method == 'DELETE':
        # Delete the user
        userDAO.delete(user_id)
        return '', 204


# Return list of artists albums 
@app.route('/api/mm/show.artist.albums/<artist_id>', methods=['GET'])
def findAlbum(artist_id):

    musix_api_call = "{}{}{}{}{}{}50&apikey={}".format(
        lyrics_api.base_url, 
        lyrics_api.artist_album_getter, 
        lyrics_api.format_url, 
        lyrics_api.p4, 
        artist_id,
        lyrics_api.p9,
        apikey)

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

    albums.sort(key=lambda d: d["album_release_date"], reverse=True)
    
    return jsonify(albums)

# Return list of artist matching the key word
@app.route('/api/mm/find.artist/<name>', methods=['GET'])
def findArtist(name):

    musix_api_call = "{}{}{}{}{}{}50&apikey={}".format(
        lyrics_api.base_url, 
        lyrics_api.artist_search, 
        lyrics_api.format_url, 
        lyrics_api.p1, 
        name, 
        lyrics_api.p9,
        apikey
    )

    response = requests.get(musix_api_call)
    data = response.json()

    artists = []

    # Build a list of dictionary objects with Artist ID and Artist Name only
    for artist in data["message"]["body"]["artist_list"]:
        artists.append({
            "artist_id":artist["artist"]["artist_id"],
            "artist_name":artist["artist"]["artist_name"]
            })

    return jsonify(artists)

if __name__=="__main__":
    app.run(debug=True)