import os
from flask import Flask, request, Response, render_template, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv

# loads environment variables from .env file
load_dotenv()

app = Flask(__name__, template_folder='public/templates')

# secret key for session management, stored in .env file
app.secret_key = os.getenv('SECRET_KEY').encode()

# gets username and password from environment variables
USERNAME = os.getenv('APP_USERNAME')
PASSWORD_HASH = generate_password_hash(os.getenv('PASSWORD'))

inventory = []

# authenticates user
def authenticate(auth):
    # checks if auth is not set to 'None' and if username and password match
    return auth and auth.username == USERNAME and check_password_hash(PASSWORD_HASH, auth.password)

@app.route('/')
def home():
    # gets authorization from request
    auth = request.authorization
    # if authentication fails, returns 401 status code
    if not authenticate(auth):
        return Response('Access denied', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    # if authentication succeeds, renders home page
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_tire():
    auth = request.authorization
    if not authenticate(auth):
        return Response('Access denied', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    section_width = aspect_ratio = rim_size = message = None
    if request.method == 'POST':
        # getters
        measurement_type = request.form.get('measurement_type')
        tire_size = request.form.get('tire_size')
        load_rating = request.form.get('load_rating')
        brand_name = request.form.get('brand_name')

        # check if any field is left blank
        if not all([measurement_type, tire_size, load_rating, brand_name]):
            message = "Error: All fields must be filled out."
        else:
            # split the tire info into section_width, aspect_ratio, and rim_size
            if measurement_type == 'metric':
                if '/' in tire_size:
                    section_width, aspect_ratio, rim_size = map(int, tire_size.split('/'))
                    # check if the tire dimensions are valid
                    if not (125 <= section_width <= 355 and str(section_width)[-1] == '5'):
                        message = "Error: Invalid section width. It should end with a 5."
                    elif not (20 <= aspect_ratio <= 90 and aspect_ratio % 5 in [0, 5]):
                        message = "Error: Invalid aspect ratio. It should end with 0 or 5."
                    elif not (14 <= rim_size <= 23):
                        message = "Error: Invalid rim size. It should be between 14 and 23."
                else:
                    message = "Error: Invalid tire size for metric measurement. It should be in the format 'width/aspect_ratio/rim_size'."
            elif measurement_type == 'imperial':
                if 'x' in tire_size:
                    section_width, aspect_ratio, rim_size = map(float, tire_size.split('x'))
                    # check if the tire dimensions are valid
                    if not (25.0 <= section_width <= 40.0):
                        message = "Error: Invalid section width. It should be between 25.0 and 40.0."
                    elif not (8.0 <= aspect_ratio <= 15.0):
                        message = "Error: Invalid aspect ratio. It should be between 8.0 and 15.0."
                    elif not (14 <= rim_size <= 23):
                        message = "Error: Invalid rim size. It should be between 14 and 23."
                else:
                    message = "Error: Invalid tire size for imperial measurement. It should be in the format 'widthxaspect_ratioxrim_size'."

            # traverses tire_brands.txt
            with open('tire_brands.txt', 'r') as f:
                tire_brands = f.read().splitlines()

            # checks if the brand name is in the list of tire brands
            if brand_name not in tire_brands:
                message = "Error: Invalid brand name"

            # if no errors, adds the tire to the inventory
            if message is None:
                tire = {
                    'measurement_type': measurement_type,
                    'section_width': section_width,
                    'aspect_ratio': aspect_ratio,
                    'rim_size': rim_size,
                    'load_rating': load_rating,
                    'brand_name': brand_name
                }
                inventory.append(tire)
                message = "Tire successfully added to inventory."

    return render_template('add.html', message=message)

@app.route('/remove', methods=['GET', 'POST'])
def remove_tire():
    auth = request.authorization
    global inventory
    if not authenticate(auth):
        return Response('Access denied', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    message = None
    if request.method == 'POST':
        # getter
        selected_tires = request.form.getlist('tire')

        if not selected_tires:
            # sets a failure message if no tires are selected
            message = "No tires selected for removal."
        else:
            # removes the selected tires from the inventory
            for tire_id in selected_tires:
                inventory = [tire for tire in inventory if tire['id'] != tire_id]

            # sets a success message
            message = "Successfully removed selected tires."

    return render_template('remove.html', inventory=inventory, message=message)

@app.route('/show_inventory', methods=['GET', 'POST'])
def search():
    auth = request.authorization
    global inventory
    if not authenticate(auth):
        return Response('Access denied', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    results = []
    if request.method == 'POST':
        # getter
        tire_size = request.form.get('tire_size')

        # splits the tire size into section_width, aspect_ratio, and rim_size
        section_width, aspect_ratio, rim_size = map(int, tire_size.split('/'))

        # searches inventory for matching tires
        results = [tire for tire in inventory if section_width - 30 <= int(tire['section_width']) <= section_width + 30 and aspect_ratio - 15 <= int(tire['aspect_ratio']) <= aspect_ratio + 15]

    return render_template('show_inventory.html', inventory=inventory)

@app.route('/logout')
def logout():
    # removes the username from the session if it's there
    session.pop('username', None)
    # redirects to home page after logout
    return redirect(url_for('home'))

if __name__ == '__main__':
    # runs the app on localhost
    app.run(host='0.0.0.0', port=80)
