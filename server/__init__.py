from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
auth = HTTPBasicAuth()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


from server import routes