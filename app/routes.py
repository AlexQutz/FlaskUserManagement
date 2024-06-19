from app import app, db, redis_client
from app.models import User
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'])

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': 'Username already exists'}), 400

    user = User(username=username, email=email, password_hash=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    user = redis_client.get(username)
    if user:
        return jsonify({'user': user.decode('utf-8')}), 200

    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    user_data = {
        'username': user.username,
        'email': user.email
    }

    redis_client.set(username, str(user_data))

    return jsonify({'user': user_data}), 200
