from flask import Blueprint, render_template, abort, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, verify_jwt_in_request
from persistence.mongoClient import Mongo
from datetime import datetime
from apis.utils import random_md5like_hash

api = Blueprint('device_management', __name__)


@api.route('/user-data/applications', methods=['GET', 'POST'])
@jwt_required
def applications():
    # verify_jwt_in_request()
    if request.method == "GET":
        db = Mongo.get_db()
        col = db["applications"]
        applications = list(col.find({"ownerId": get_jwt_identity()}, {'_id': 0}))
        return jsonify(applications=applications), 200
    if request.method == "POST":
        try:
            dt = request.get_json()
            dt["hasAppKey"] = False if dt["appKey"] == "" else True
            dt["ownerId"] = get_jwt_identity()
            dt["dateCreated"] = datetime.now()
            dt["devices"] = []
            dt["appId"] = random_md5like_hash(6)
            db = Mongo.get_db()
            col = db["applications"]
            if col.insert_one(dt).acknowledged:
                return jsonify(msg="ok"), 200
            else:
                return jsonify(msg="Bad Gateway"), 501
        except Exception:
            return jsonify(msg="Bad Gateway"), 501


@api.route('/gateways/<appId>', methods=['GET', 'POST'])
@jwt_required
def gateways(appId):
    if request.method == "GET":
        db = Mongo.get_db()
        col = db["gateways"]
        gateways = list(col.find({"appId": appId}, {'_id': 0}))
        return jsonify(gateways=gateways), 200
    if request.method == "POST":
        try:
            db = Mongo.get_db()
            col = db["gateways"]
            dt = request.get_json()
            dt["appId"] = appId
            dt["ownerId"] = get_jwt_identity()
            dt["dateCreated"] = datetime.now()
            if col.insert_one(dt).acknowledged:
                col = db["applications"]
                if col.update_one({"appId": appId}, {"$push": {"gateways": dt["gwId"]}}, upsert=True).modified_count:
                    return jsonify(msg="ok"), 200
                else:
                    return jsonify(msg="Bad Gateway"), 501
            else:
                return jsonify(msg="Bad Gateway"), 501
        except Exception as e:
            return jsonify(msg="Bad Gateway"), 501