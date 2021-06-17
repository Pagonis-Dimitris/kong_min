from flask import Flask, jsonify
from flask_caching import Cache
from flask_cors import CORS
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError


app = Flask(__name__)
CORS(app)

app.config["CACHE_TYPE"] = "SimpleCache"
# app.config["CACHE_DIR"] = "/cache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:mypass@db/mydb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)
bcrypt = Bcrypt(app)

db = SQLAlchemy()
ma = Marshmallow()
cache = Cache(app)

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

