from flask import Blueprint, render_template, abort, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
import hashlib
from persistence.mongoClient import Mongo

api = Blueprint('user', __name__)

fake_user = [{"username": "test@tlas", "password": "71f78bda76e73d5b97a30b22f226dcd7"}]


@api.route('/users/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    if (not ("password" in data.keys() and "username" in data.keys())):
        abort(400)
    data["password"] =hashlib.md5(data["password"].encode()).hexdigest()

    db = Mongo.get_db()
    col = db["auth"]
    if(not col.find(data).count()):
        abort(404)
    access_token = create_access_token(identity=data["username"])
    return jsonify(access_token=access_token), 200
