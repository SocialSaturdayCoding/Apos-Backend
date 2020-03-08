import sys

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
if "pytest" in sys.modules:
    app.config.from_object('apos.config_test.Config')
else:
    app.config.from_object('apos.config.Config')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy()
db.init_app(app)
bcrypt = Bcrypt()
jwt = JWTManager(app)
api = Api(app)
