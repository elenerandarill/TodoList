from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user
from . import app, db, bcrypt, login_manager
from .forms import RegisterForm, LoginForm
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
        flash("Your account has been created.", "success")
        return redirect(url_for('home'))
    return render_template("register.html", title=title, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = "Login"
    form = LoginForm()
    if form.validate_on_submit():
        # Conditon 1 - is email in db.
        user = User.query.filter_by(email=form.email.data).first()
        # Condition 2 - is password correct.
        password = bcrypt.check_password_hash(user.password_hash, form.password.data)
        # if True and True:
        if user and password:
            # From flask-login module "login_user".
            login_user(user, remember=form.remember.data)
            # 'request.args' returns dictionary, so we get one key value by passing "next".
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login or password incorrect.", "danger")
    return render_template("login.html", title=title, form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)