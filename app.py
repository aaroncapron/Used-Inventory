from flask import Flask, request, Response, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)

USERNAME = 'txe_01'
PASSWORD_HASH = generate_password_hash('used')

# A simple in-memory data store for the example
inventory = []

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == USERNAME and check_password_hash(PASSWORD_HASH, auth.password)):
            return Response('Access denied', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@auth_required
def home():
    return "Signing in . . ."

@app.route('/inventory', methods=['GET'])
@auth_required
def get_inventory():
    return jsonify(inventory)

@app.route('/inventory', methods=['POST'])
@auth_required
def add_item():
    item = request.json
    inventory.append(item)
    return jsonify(item), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
