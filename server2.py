from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/database'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

@app.route('/api/users', methods=['GET', 'POST'])
def api_users():
    if request.method == 'GET':
        # Return a list of users
        users = User.query.all()
        return jsonify([{'id': user.id, 'name': user.name} for user in users])
    elif request.method == 'POST':
        # Create a new user
        data = request.get_json()
        user = User(name=data['name'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'id': user.id, 'name': user.name}), 201

@app.route('/api/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def api_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return 'User not found', 404
    if request.method == 'GET':
        # Return the user
        return jsonify({'id': user.id, 'name': user.name})
    elif request.method == 'PUT':
        # Update the user
        data = request.get_json()
        user.name = data['name']
        db.session.commit()
        return jsonify({'id': user.id, 'name': user.name})
    elif request.method == 'DELETE':
        # Delete the user
        db.session.delete(user)
        db.session.commit()
        return '', 204
