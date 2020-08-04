from flask import Blueprint, render_template, abort, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity, verify_jwt_in_request
from config.configuration import Configuration
from datetime import datetime, timezone
from persistence.utils import *
from .utils import *
from test_data.debugResponse import debugResponse
import json
api = Blueprint('open_data', __name__)


@api.route('/openData', methods=['GET'])
def openData():
    config = Configuration.get()
    if request.method == "GET":
        data = request.values
        if not data.has_key('source'):
            return jsonify({"msg": "Source API not provided"}), 400
        source = data.get('source')
        if source not in config["OPEN_DATA"]["SOURCES"]:
            return jsonify({"msg": "Unknown open data source"}), 400
        apiresponse = None
        if(config["DEBUG"]):
            apiresponse = debugResponse(source)
        else:
            if source == 'openweathermap':
                apiresponse = openweathermap()
            if source == 'weatherapi':
                apiresponse = weatherapi()
            if source == "weatherstack":
                apiresponse = weatherstack()
        if apiresponse.status_code != 200:
            print("log the error")
            abort(500)
        return jsonify(json.loads(apiresponse.text)), 200

@api.route('/openData/rating', methods=['GET', 'POST'])
@jwt_required
def ratings():
    if request.method == "POST":
        try:
            verify_jwt_in_request()
            id = get_jwt_identity()
            data = request.get_json()
            if ("rate" not in data):
                return jsonify({"msg": "Ratings are missing"}), 400
            if ("data" not in data):
                return jsonify({"msg": "API data are missing"}), 400
            if ("source" not in data):
                return jsonify({"msg": "API source is missing"}), 400
            data["created_on"] = datetime.now(timezone.utc)
            data["userId"] = id
            if saveRating(data):
                return jsonify({"msg": "OK"}), 200
            print("log")
            abort(400)
        except Exception as e:
            print("log", str(e))
            abort(500)