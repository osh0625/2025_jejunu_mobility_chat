from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your-secret-key'

chats = {}

    
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('chat'))
    
    return render_template('login.html')

@app.route('/chat')
def chat():
    user_chat = chats.get(session['username'], [])
    return render_template('chat.html',
                           username = session['username'],
                           chats = user_chat)


@app.route('/add', methods = ['POST'])
def add_chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    new_chat = request.form['chat']
    if new_chat:
        if session['username'] not in chats:
            chats[session['username']] = []
        chats[session['username']].append(new_chat)
    
    return redirect(url_for('chat'))

if __name__ == '__main__':
    app.run(debug = True)