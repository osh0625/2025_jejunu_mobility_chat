from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
socketio = SocketIO(app)

messages = []

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', messsages=messages, name = session['username'])

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('index'))

    return render_template('login.html')

@socketio.on('message')
def handle_message(data):
    message = {
        'user' : session['username'],
        'message' : data['message']
    }
    messages.append(message)
    emit('message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)