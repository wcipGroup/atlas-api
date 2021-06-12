from flask import Blueprint, render_template, abort, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, verify_jwt_in_request
import hashlib
import time
from datetime import datetime, timezone, timedelta
from persistence.mongoClient import Mongo
import json
from amqp.publisher import Publisher

api = Blueprint('user', __name__)

fake_user = [{"username": "test@tlas", "password": "71f78bda76e73d5b97a30b22f226dcd7"}]


@api.route('/users/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    if (not ("password" in data.keys() and "username" in data.keys())):
        return "Bad Call", 400
    data["password"] =hashlib.md5(data["password"].encode()).hexdigest()

    db = Mongo.get_db()
    col = db["auth"]
    if not col.find(data).count():
        return "Not Found", 404
    access_token = create_access_token(identity=data["username"], expires_delta=timedelta(days=30))
    return jsonify(access_token=access_token, identity=data["username"]), 200


@api.route('/users/newPass/<userId>', methods=['POST'])
@jwt_required
def changePassword(userId):
    data = request.get_json()
    if not ("password" in data.keys()):
        return "Bad Call", 400
    data["password"] =hashlib.md5(data["password"].encode()).hexdigest()
    db = Mongo.get_db()
    col = db["auth"]
    col.update({"username": userId}, {"$set": {"password": data["password"]}})
    # if not col.find(data).count():
    #     return "Not Found", 404
    # access_token = create_access_token(identity=data["username"], expires_delta=timedelta(days=30))
    # return jsonify(access_token=access_token, identity=data["username"]), 200
    return jsonify(data="okk"), 200


@api.route('/user-data/applications/<userId>', methods=['GET', 'POST'])
@jwt_required
def getAppcilations(userId):
    # verify_jwt_in_request()
    if request.method == "GET":
        if not userId:
            return "Bad Call", 400
        db = Mongo.get_db()
        col = db["applications"]
        applications = list(col.find({"ownerId": userId}, {'_id': 0}))
        return jsonify(applications=applications), 200
    if request.method == "POST":
        try:
            dt = request.get_json()
            dt["hasAppKey"] = False if dt["appKey"] == "" else True
            # dt["ownerId"] = get_jwt_identity()
            dt["ownerId"] = userId
            dt["dateCreated"] = datetime.now()
            dt["devices"] = []
            db = Mongo.get_db()
            col = db["applications"]
            if col.insert_one(dt).acknowledged:
                return jsonify(msg="ok"), 200
            else:
                return jsonify(msg="Bad Gateway"), 501
        except Exception:
            return jsonify(msg="Bad Gateway"), 501


@api.route('/user-data/profile/<userId>', methods=['GET', 'POST'])
@jwt_required
def getProfile(userId):
    if request.method == "GET":
        if not userId:
            return "Bad Call", 400
        db = Mongo.get_db()
        col = db["profile"]
        profile = list(col.find({"username": userId}, {'_id': 0}))
        if len(profile):
            return jsonify(profile=profile[0]), 200
        return "Not found", 404
    if request.method == "POST":
        data = request.get_json()
        if not ("autoActions" in data.keys() and "autoActionsTimePeriod" in data.keys()):
            return "Bad Call", 400
        db = Mongo.get_db()
        col = db["profile"]
        if col.update_one({"username": userId},
                          {"$set": {"autoActions": data["autoActions"],
                                    "autoActionsTimePeriod": data["autoActionsTimePeriod"]}
                           }, upsert=True).acknowledged:
            return jsonify(msg="ok"), 200
        else:
            return jsonify(msg="Bad Gateway"), 501


@api.route('/user-data/devices/<appId>', methods=['GET', 'POST'])
@jwt_required
def getDevices(appId):
    if request.method == "GET":
        db = Mongo.get_db()
        col = db["devices"]
        devices = list(col.find({"appId": appId}, {'_id': 0}))
        return jsonify(devices=devices), 200
    if request.method == "POST":
        try:
            db = Mongo.get_db()
            col = db["devices"]
            dt = request.get_json()
            dt["appId"] = appId
            dt["ownerId"] = get_jwt_identity()
            dt["dateCreated"] = datetime.now()
            if col.insert_one(dt).acknowledged:
                col = db["applications"]
                if col.update_one({"appId": appId}, {"$push": {"devices": dt["devAddr"]}}, upsert=True).modified_count:
                    return jsonify(msg="ok"), 200
                else:
                    return jsonify(msg="Bad Gateway"), 501
            else:
                return jsonify(msg="Bad Gateway"), 501
        except Exception:
            return jsonify(msg="Bad Gateway"), 501


@api.route('/user-data/devices-by-owner/<ownerId>', methods=['GET', 'POST'])
@jwt_required
def getDevicesByOwner(ownerId):
    db = Mongo.get_db()
    col = db["devices"]
    devices = list(col.find({"ownerId": ownerId}, {'_id': 0}))
    return jsonify(devices=devices), 200


@api.route('/user-data/data/<devAddr>', methods=['GET'])
def getData(devAddr):
    db = Mongo.get_db()
    col = db["device_raw_data"]
    sensor_data = list(col.find({"devAddr": devAddr, "msgType": "04"}, {"_id": 0}))
    return jsonify(data=sensor_data), 200


@api.route('/user-data/status/<devAddr>', methods=['GET'])
def getStatus(devAddr):
    db = Mongo.get_db()
    col = db["device_raw_data"]
    status = list(col.find({"devAddr": devAddr, "msgType": "04"}, {"_id": 0}).sort([("date", -1)]).limit(1))
    return jsonify(status=status), 200


@api.route('/user-action/<ownerId>', methods=['POST'])
def action(ownerId):
    data = request.get_json()
    mqttc = Mongo.get_mqttc()
    mqttc.publish('atlas/action', json.dumps(data))
    print(data)
    return "ok", 200


@api.route('/user-data/<devAddr>/interval', methods=['GET', 'POST'])
def deviceInterval(devAddr):
    if request.method == "POST":
        try:
            dt = request.get_json()
            interval = dt["interval"]
            db = Mongo.get_db()
            col = db["downlink_mac"]
            col.update({"devAddr": devAddr},
                       {"$set": {"interval": {"commandType": "interval", "commandId": 1,
                                 "value":  interval, "dateCreated": datetime.now(),
                                 "status": "pending"}}},
                       upsert=True)
        except Exception:
            return jsonify(msg="Bad Gateway"), 501
        return jsonify(msg="ok"), 200
    if request.method == "GET":
        try:
            db = Mongo.get_db()
            col = db["downlink_mac"]
            downlink_mac = list(col.find({"devAddr": devAddr}))
            if len(downlink_mac):
                if downlink_mac[0]['interval']:
                    return jsonify(interval=downlink_mac[0]['interval']), 200
            return jsonify(interval=20), 200
        except Exception:
            return jsonify(msg="Bad Gateway"), 501
