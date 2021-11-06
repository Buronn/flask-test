from flask import Flask, request, jsonify, session

from . import create_app
from .models import User
app = create_app()
app.secret_key = 'super secret key'

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        session['username'] = username
        return jsonify({
            'status': 'success',
            'message': 'Logged in successfully.',
            'token': user.generate_token()
        })
    else:
        return jsonify({
            'status': 'fail',
            'message': 'Invalid username or password.'
        })


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']
    career = data['career']
    semestre = data['semestre']

    user = User.query.filter_by(username=username).first()

    if user:
        return jsonify({
            'status': 'fail',
            'message': 'Username already exists.'
        })
    else:
        user = User(username=username, email=email, career=career, semestre=semestre)
        user.set_password(password)
        user.save()
        return jsonify({
            'status': 'success',
            'message': 'Registered successfully.',
            'token': user.generate_token()
        })
