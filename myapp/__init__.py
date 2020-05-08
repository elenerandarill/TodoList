#!/usr/bin/python3
from flask import Flask


app = Flask(__name__)
app.config["SECRET_KEY"] = '2d65c65e323654552be29cc808a58eab'


from myapp import routes