from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from apis import app as application
import os
from config.configuration import Configuration
from persistence.mongoClient import Mongo
application.config['JWT_SECRET_KEY'] = 'dsakjlrew@#RSdf'
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=2)
application.config['JWT_ALGORITHM'] = 'HS384'
application.config['CORS_HEADERS'] = 'Content-Type'
jwt = JWTManager(application)
cors = CORS(application)

@application.errorhandler(400)
def _handle_api_error(ex):
    print(ex)
    return jsonify({"msg": "Bad Request"}), 400


@application.errorhandler(404)
def _handle_api_error(ex):
    print(ex)
    return jsonify({"msg": "Not Found"}), 404


@application.errorhandler(500)
def _handle_api_error(ex):
    print(ex)
    return jsonify({"msg": "Bad Gateway"}), 500



@jwt.unauthorized_loader
def my_unauthorized_loader(token):
    return jsonify({"msg": "No JWT token"}), 401


@jwt.invalid_token_loader
def my_invalid_token_loader(token):
    return jsonify({"msg": "Invalid JWT token"}), 422


# if i want to make a custom return for get_jwt_identity
# @jwt.user_identity_loader
# def user_identity_lookup(user):
#     return user['id']


if __name__ == "__main__":
    try:
        cwd = os.path.dirname(os.path.abspath(__file__))
        Configuration(os.path.join(cwd, 'config/config.json'))
        config = Configuration.get()
        db = Mongo()
    except Exception as e:
        raise SystemExit("Error while setting communications: {}".format(str(e)))

    application.run(debug=config["DEBUG"])
