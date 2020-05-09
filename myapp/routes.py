from flask import render_template, url_for, redirect
from . import app, db, bcrypt
from .forms import RegisterForm
from myapp.models import User, Task


@app.route('/')
@app.route('/home')
def home():
    title = "Home Page"
    return render_template("home.html", title=title)


@app.route('/register', methods=['GET', 'POST'])
def register():
    title = "Registration"
    form = RegisterForm()
    if form.validate_on_submit():
        password_hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(uname=form.uname.data, email=form.email.data, password_hash=password_hashed)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("register.html", title=title, form=form)
