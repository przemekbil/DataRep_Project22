from flask import Flask, jsonify, abort

app = Flask(__name__, static_url_path='', static_folder='static_pages')




if __name__=="__main__":
    app.run(debug=True)