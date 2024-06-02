import os
from flask import Flask, request, Response, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv

load_dotenv() # takes environment variables from .env file

app = Flask(__name__, template_folder='public/templates')

USERNAME = os.getenv('APP_USERNAME')
PASSWORD_HASH = generate_password_hash(os.getenv('PASSWORD'))

# Placeholder for the inventory
inventory = []

def authenticate(auth):
    return auth and auth.username == USERNAME and check_password_hash(PASSWORD_HASH, auth.password)

@app.route('/')
def home():
    auth = request.authorization
    if not authenticate(auth):
        return Response('Access denied', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_tire():
    auth = request.authorization
    if not authenticate(auth):
        return Response('Access denied', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    if request.method == 'POST':
        tire = request.form.get('tire')
        inventory.append(tire)
    return render_template('add.html')

@app.route('/remove', methods=['GET', 'POST'])
def remove_tire():
    auth = request.authorization
    if not authenticate(auth):
        return Response('Access denied', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    if request.method == 'POST':
        tire = request.form.get('tire')
        inventory.remove(tire)
    return render_template('remove.html')

@app.route('/search', methods=['GET', 'POST'])
def search_by_size():
    auth = request.authorization
    if not authenticate(auth):
        return Response('Access denied', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    if request.method == 'POST':
        size = request.form.get('size')
        results = [tire for tire in inventory if tire.size == size]
    return render_template('search.html')

@app.route('/show')
def show_inventory():
    auth = request.authorization
    if not authenticate(auth):
        return Response('Access denied', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    return render_template('show.html', inventory=inventory)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
