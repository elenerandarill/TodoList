from flask import render_template, url_for
from myapp import app
from myapp.forms import RegisterForm


@app.route('/')
@app.route('/home')
def index():
    title = "Home Page"
    return render_template("home.html", title=title)

@app.route('/register')
def register():
    form = RegisterForm()
    return render_template("register.html", form=form)
