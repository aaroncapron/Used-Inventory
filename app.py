import os
from flask import Flask, request, Response, render_template, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

app = Flask(__name__, template_folder='public/templates')

# secret key for session management
app.secret_key = os.getenv('SECRET_KEY').encode()

# gets username and password from environment variables
USERNAME = os.getenv('APP_USERNAME')
PASSWORD_HASH = generate_password_hash(os.getenv('PASSWORD'))

inventory = []

# authenticates user
def authenticate(auth):
    # Check if auth is not None and if username and password match
    return auth and auth.username == USERNAME and check_password_hash(PASSWORD_HASH, auth.password)

@app.route('/')
def home():
    # get authorization from request
    auth = request.authorization
    # if authentication fails, return 401 status code
    if not authenticate(auth):
        return Response('Access denied', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    # if authentication succeeds, render home page
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_tire():
    auth = request.authorization
    if not authenticate(auth):
        return Response('Access denied', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    # if request method is POST, get tire details from form and add to inventory
    if request.method == 'POST':
        measurement_type = request.form.get('measurement_type')
        section_width = request.form.get('section_width')
        aspect_ratio = request.form.get('aspect_ratio')
        rim_size = request.form.get('rim_size')
        load_rating = request.form.get('load_rating')
        tire = {
            'measurement_type': measurement_type,
            'section_width': section_width,
            'aspect_ratio': aspect_ratio,
            'rim_size': rim_size,
            'load_rating': load_rating
        }
        inventory.append(tire)
    return render_template('add.html')

@app.route('/remove', methods=['GET', 'POST'])
def remove_tire():
    auth = request.authorization
    if not authenticate(auth):
        return Response('Access denied', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    # if request method is POST, get tire details from form and remove from inventory
    if request.method == 'POST':
        tire = request.form.get('tire')
        inventory.remove(tire)
    return render_template('remove.html')

@app.route('/search', methods=['GET', 'POST'])
def search_by_size():
    auth = request.authorization
    if not authenticate(auth):
        return Response('Access denied', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    # if request method is POST, get size from form and search inventory
    if request.method == 'POST':
        size = request.form.get('size')
        results = [tire for tire in inventory if tire['size'] == size]
    return render_template('search.html', results=results)

@app.route('/show')
def show_inventory():
    auth = request.authorization
    if not authenticate(auth):
        return Response('Access denied', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    # render show page with all items in inventory
    return render_template('show.html', inventory=inventory)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    # redirect to home page after logout
    return redirect(url_for('home'))

if __name__ == '__main__':
    # run the app on host 0.0.0.0 and port 80
    app.run(host='0.0.0.0', port=80)
