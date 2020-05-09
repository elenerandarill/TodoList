#!/usr/bin/python3
import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = '2d65c65e323654552be29cc808a58eab'
# In this program using 'flask-migrate' by Miguel Grinberg...
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///dbase.db'
# Turns off notifications about DB changes that are going to be made.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# To make password hashes.
bcrypt = Bcrypt(app)


from . import routes, models