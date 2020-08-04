from flask import Flask

from .openData import api as bp1
from .users import api as bp2

app = Flask(__name__)
app.register_blueprint(bp1)
app.register_blueprint(bp2)


# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
