# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the app
app = Flask(__name__, instance_relative_config=True)
app.config["SECRET_KEY"] = 'secret-key'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///studio_ghiblis_moviemaker.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.app_context().push()

# Load the config file
app.config.from_object('config')


# Load the views
from app import app
from app import models