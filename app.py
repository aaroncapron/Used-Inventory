import os
from flask import Flask, request, Response, render_template, session, redirect, url_for
from firebase_admin import credentials, firestore, initialize_app
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv

# loads environment variables from .env file
load_dotenv()

# Initialize Firestore with environment variables
cred = credentials.Certificate({
    "type": os.getenv('FIREBASE_TYPE'),
    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
    "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
    "token_uri": os.getenv('FIREBASE_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_X509_CERT_URL')
})
default_app = initialize_app(cred)
db = firestore.client()

app = Flask(__name__, template_folder='public/templates')

# secret key for session management, stored in .env file
app.secret_key = os.getenv('SECRET_KEY').encode()

# gets username and password from environment variables
USERNAME = os.getenv('APP_USERNAME')
PASSWORD_HASH = generate_password_hash(os.getenv('PASSWORD'))

inventory = []
sku = 1000  # initialize SKU

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

    # gets the latest 5 tires from firestore
    docs = db.collection('tires').order_by('sku', direction=firestore.Query.DESCENDING).limit(5).stream()
    latest_tires = [doc.to_dict() for doc in docs]

    return render_template('home.html', latest_tires=latest_tires)

@app.route('/add', methods=['GET', 'POST'])
def add_tire():
    global sku
    auth = request.authorization
    if not authenticate(auth):
        return Response('Access denied', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    brand_name = measurement_type = tire_size = load_rating = message = None
    if request.method == 'POST':
        # getters
        measurement_type = request.form.get('measurement_type')
        tire_size = request.form.get('tire_size')
        load_rating = request.form.get('load_rating')
        brand_name = request.form.get('brand_name')
        brand_name = brand_name.lower()

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
                'sku': sku,
                'measurement_type': measurement_type,
                'section_width': section_width,
                'aspect_ratio': aspect_ratio,
                'rim_size': rim_size,
                'load_rating': load_rating,
                'brand_name': brand_name
            }
        db.collection('tires').document(str(sku)).set(tire)
        sku += 1  # increment SKU
        message = "Tire successfully added to inventory."

    return render_template('add.html', message=message)

@app.route('/remove', methods=['GET', 'POST'])
def remove_tire():
    auth = request.authorization
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
            for tire_sku in selected_tires:
                # Remove tire from Firestore
                db.collection('tires').document(tire_sku).delete()

            # sets a success message
            message = "Successfully removed selected tires."

    return render_template('remove.html', inventory=inventory, message=message)

@app.route('/show_inventory', defaults={'page_num': 1})
@app.route('/show_inventory/<int:page_num>', methods=['GET', 'POST'])
def show_inventory(page_num):
    auth = request.authorization
    if not authenticate(auth):
        return Response('Access denied', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    results = []
    if request.method == 'POST':
        # tire size getter
        tire_size = request.form.get('tire_size')

        # splits the tire size into section_width, aspect_ratio, and rim_size
        section_width, aspect_ratio, rim_size = map(int, tire_size.split('/'))

        # searches inventory for matching tires
        results = [tire for tire in inventory if section_width - 30 <= int(tire['section_width']) <= section_width + 30 and aspect_ratio - 15 <= int(tire['aspect_ratio']) <= aspect_ratio + 15]

    # gets number of items per page from request, defaults to 10
    items_per_page = request.args.get('items_per_page', 10, type=int)

    # calculates start and end indices for items on page
    start = (page_num - 1) * items_per_page
    end = start + items_per_page

    # Fetch data from Firestore
    docs = db.collection('tires').stream()
    inventory = [doc.to_dict() for doc in docs]

    # page items getter
    page_items = inventory[start:end]

    return render_template('show_inventory.html', inventory=page_items, page_num=page_num)

@app.route('/logout')
def logout():
    # removes the username from the session if it's there
    session.pop('username', None)
    # redirects to home page after logout
    return redirect(url_for('home'))

if __name__ == '__main__':
    # runs the app on localhost
    app.run(host='0.0.0.0', port=80)
