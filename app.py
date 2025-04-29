from flask import Flask, render_template, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Keep this secret in real apps
USER_FILE = 'users.txt'

def save_user(username, password):
    with open(USER_FILE, 'a') as f:
        f.write(f"{username},{password}\n")

def check_user(username, password):
    try:
        with open(USER_FILE, 'r') as f:
            for line in f:
                stored_user, stored_pass = line.strip().split(',')
                if stored_user == username and stored_pass == password:
                    return True
        return False
    except FileNotFoundError:
        return False

def get_user_file(username):
    return f"data_{username}.txt"

def get_saved_data(username):
    user_file = get_user_file(username)
    if os.path.exists(user_file):
        with open(user_file, 'r') as f:
            return f.read()
    return None

def save_data(username, data):
    user_file = get_user_file(username)
    with open(user_file, 'a') as f:
        f.write(data + '\n')

def delete_data(username):
    user_file = get_user_file(username)
    if os.path.exists(user_file):
        os.remove(user_file)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if check_user(username, password):
        session['user'] = username
        return redirect(url_for('dashboard'))
    else:
        return "<h3>Login failed. <a href='/'>Try again</a></h3>"

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    
    save_user(username, password)
    return "<h3>Registered successfully. <a href='/'>Login now</a></h3>"

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))

    username = session['user']
    saved_data = get_saved_data(username)

    if request.method == 'POST':
        data = request.form['data']
        save_data(username, data)
        message = "Data saved successfully!"
        message_type = "success"
        return render_template('dashboard.html', username=username, saved_data=get_saved_data(username), message=message, message_type=message_type)

    return render_template('dashboard.html', username=username, saved_data=saved_data)

@app.route('/delete_data', methods=['POST'])
def delete_data_route():
    if 'user' not in session:
        return redirect(url_for('home'))

    username = session['user']
    delete_data(username)

    message = "Your saved data has been deleted."
    message_type = "error"
    return render_template('dashboard.html', username=username, saved_data=None, message=message, message_type=message_type)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
