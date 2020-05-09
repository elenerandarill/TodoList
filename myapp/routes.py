from flask import render_template, url_for
from . import app
from .forms import RegisterForm


@app.route('/')
@app.route('/home')
def index():
    title = "Home Page"
    return render_template("home.html", title=title)


@app.route('/register', methods=['GET', 'POST'])
def register():
    title = "Registration"
    form = RegisterForm()
    return render_template("register.html", title=title, form=form)
