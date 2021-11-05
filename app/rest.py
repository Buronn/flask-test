import pymysql
import hashlib
from flask import request, jsonify, render_template, session
from app import app
from db import mysql
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as' + session['username']
    else:
        return 'You are not logged in'


@app.route('/api/login', methods=['POST'])
def login():
    if request.json is None:
        return jsonify({'error': 'No data found'})
    if 'username' not in request.json or 'password' not in request.json:
        return jsonify({'error': 'No username or password found'})
    if session.get('username') is not None:
        return jsonify({'error': 'Already logged in'})
    username = request.json['username']
    password = request.json['password']
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM user")
    rows = cursor.fetchall()
    hash_pass = hashlib.sha256(password.encode('utf-8')).hexdigest()
    for row in rows:
        if row['username'] == username and row['password'] == hash_pass:
            session['username'] = username
            return jsonify({'message': 'Login success!'})
    return jsonify({'message': 'Login failed!'})

@app.route('/api/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM user")
    rows = cursor.fetchall()
    for row in rows:
        if row['username'] == username:
            return jsonify({'message': 'Username already exists!'})
        if row['email'] == email:
            return jsonify({'message': 'Email already exists!'})
    sql = "INSERT INTO user (username, password,email) VALUES (%s, SHA2(%s,256),%s)"
    cursor.execute(sql, (username, password, email))
    conn.commit()
    return jsonify({'message': 'Register success!'})

@app.route('/api/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logout success!'})

@app.route('/api/get_user/<username>', methods=['GET'])
def get_user(username):
    if session.get('username') is None:
        return jsonify({'error': 'Not logged in'})
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM user WHERE username = %s", username)
    row = cursor.fetchone()
    if row is None:
        return jsonify({'error': 'User not found'})
    return jsonify(row)

@app.route('/api/get_all_user', methods=['GET'])
def get_all_user():
    if session.get('username') is None:
        return jsonify({'error': 'Not logged in'})
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM user")
    rows = cursor.fetchall()
    return jsonify(rows)

@app.route('/api/delete_user/<username>', methods=['GET'])
def delete_user(username):
    if session.get('username') is None:
        return jsonify({'error': 'Not logged in'})
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("DELETE FROM user WHERE username = %s", username)
    conn.commit()
    if cursor.rowcount == 0:
        return jsonify({'error': 'User not found'})
    return jsonify({'message': 'Delete success!'})

@app.route('/api/update_email/<username>', methods=['POST'])
def update_email(username):
    if session.get('username') is None:
        return jsonify({'error': 'Not logged in'})
    email = request.json['email']
    if email is None:
        return jsonify({'error': 'No email found'})
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM user WHERE username = %s", username)
    row = cursor.fetchone()
    if row['email'] == email:
        return jsonify({'error': 'Use another email'})
    if row is None:
        return jsonify({'error': 'User not found'})
    sql = "UPDATE user SET email = %s WHERE username = %s"
    cursor.execute(sql, (email, username))
    conn.commit()
    return jsonify({'message': 'Update success!'})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
