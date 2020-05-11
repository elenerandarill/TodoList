#!/usr/bin/python3
import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
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

login_manager = LoginManager()
login_manager.init_app(app)


from . import routes, models

"""But with database migration support, after you modify the models in your application
you generate a new migration script (flask db migrate), you probably review it to make
sure the automatic generation did the right thing, and then apply the changes to your 
development database (flask db upgrade). You will add the migration script to source 
control and commit it.(flask db downgrade) command undoes the last migration. 
You can downgrade the database, delete the migration script, and then generate a new one to replace it"""