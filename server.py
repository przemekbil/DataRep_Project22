from flask import Flask, jsonify, request, abort
import config, lyrics_api, requests, json
from projectDAO import userDAO, favoritesDAO

app = Flask(__name__, static_url_path='', static_folder='static_pages')

# API key for Musixmathc server
apikey = config.musicMatch["apiKey"]


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

# Return list of registered profiles
@app.route('/api/users', methods=['GET'])
def getUsers():

    users = userDAO.getAll()
    return jsonify(users)

# Add new user
@app.route('/api/user', methods=['PUT'])
def new_user():
    data = request.get_json(force=True)
    #print("This is what we got from the site: {}".format(data))
    name = data['name']
    newId = userDAO.create(name)
    user = userDAO.findByID(newId)
    return jsonify(user)

# Add new favorite album to user profile
@app.route('/api/addfav', methods=['PUT'])
def add_favorite():
    # add new user
    data = request.get_json(force=True)
    #print("This is what we got from the site: {}".format(data))
    u_id = data['user_id']
    album_id = data['album_id']

    newId = favoritesDAO.create(u_id, album_id)

    return jsonify({'fav_id':newId})


# Remove album form favorites
@app.route('/api/fav', methods=['DELETE'])
def rem_favorite():
    
    data = request.get_json(force=True)
    fav_id = data['id']

    favoritesDAO.delete(fav_id)

    return jsonify({'OK': 200})

# Get user favorites
@app.route('/api/userfavs/<int:user_id>', methods=['GET'])
def get_user_favs(user_id):
    
    user = userDAO.findByID(user_id)

    # check if user exists
    if user is None:
        return 'User not found', 404
    

    user_favs = favoritesDAO.getFavoritesByUserID(user_id)    

    for fav in user_favs:

        # Get the albums details form Musixmatch server
        musix_api_call = "{}{}{}{}{}&apikey={}".format(
        lyrics_api.base_url, 
        lyrics_api.album_getter, 
        lyrics_api.format_url, 
        lyrics_api.p5, 
        fav['album_id'],
        apikey)

        response = requests.get(musix_api_call)
        data = response.json()

        fav['album_name'] = data["message"]["body"]["album"]["album_name"]
        fav["album_release_date"] = data["message"]["body"]["album"]["album_release_date"]
        fav["artist_name"]= data["message"]["body"]["album"]["artist_name"]
        fav["album_label"] = data["message"]["body"]["album"]["album_label"]


    return jsonify(user_favs)


# Display, update or delete selected user
# If user is deleted, all his/her favorites iwll be deleted too
@app.route('/api/user/<int:user_id>', methods=['GET', 'PUT', 'POST', 'DELETE'])
def api_user(user_id):

    user = userDAO.findByID(user_id)

    if user is None:
        return 'User not found', 404
    if request.method == 'GET':
        # Return the user
        return jsonify(user)
    
    elif request.method == 'POST':
        # Update the user
        data = request.get_json(force=True)
        name = data['name']
        userDAO.update(name, user_id)
        user = userDAO.findByID(user_id)
        return jsonify(user)

    elif request.method == 'DELETE':
        # Delet all users favorites first
        favoritesDAO.deleteUserFavorites(user_id)
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