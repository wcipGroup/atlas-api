import random
import string
from functools import wraps

import requests
from config.configuration import Configuration
from flask import jsonify
from flask_jwt_extended import get_jwt_claims


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt_claims()
        if claims['role'] != 'admin':
            return jsonify({"msg": "Admin required"}), 403
        else:
            return fn(*args, **kwargs)

    return wrapper()


def openweathermap():
    config = Configuration.get()
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {}
    params["q"] = config["OPEN_DATA"]["TOWN"]
    params["appid"] = config["OPEN_DATA"]["OPEN_WEATHER_MAP"]["KEY"]
    r = requests.get(url, params)
    return r


def weatherapi():
    config = Configuration.get()
    url = "http://api.weatherapi.com/v1/current.json"
    params = {}
    params["q"] = config["OPEN_DATA"]["TOWN"]
    params["key"] = config["OPEN_DATA"]["WEATHER_API"]["KEY"]
    r = requests.get(url, params)
    return r


def weatherstack():
    config = Configuration.get()
    url = "http://api.weatherstack.com/current"
    params = {}
    params["query"] = config["OPEN_DATA"]["TOWN"]
    params["access_key"] = config["OPEN_DATA"]["WEATHER_STACK"]["KEY"]
    r = requests.get(url, params)
    return r


def findIndexOfActuator(data):
    if data["action"] == "feeder": return 0
    if data["action"] == "alarm": return 2
    if data["action"] == "oxygen": return 4
    if data["action"] == "coldWater": return 6
    if data["action"] == "hotWater": return 8
    if data["action"] == "acid": return 10
    if data["action"] == "base": return 12
    raise Exception


def random_md5like_hash(length):
    available_chars = string.hexdigits[:16]
    return ''.join(
        random.choice(available_chars)
        for dummy in range(length))
