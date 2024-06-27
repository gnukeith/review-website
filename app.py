from flask import Flask, render_template, request, redirect, url_for, session
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load admin credentials from environment variables
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'securepassword')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('admin'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/admin')
def admin():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('login'))

@app.route('/browser/<name>')
def browser(name):
    templates = {
        'firefox': 'browsers/firefox.html',
        'brave': 'browsers/brave.html',
        'vanadium': 'browsers/vanadium.html'
    }

    template = templates.get(name, None)
    if template:
        return render_template(template)
    else:
        return render_template('404.html'), 404

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
