from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import app, db, bcrypt, login_manager
from .forms import RegisterForm, LoginForm, AddTaskForm
from myapp.models import User, Task


@app.route('/')
@app.route('/home')
def home():
    title = "Home Page"
    return render_template("home.html", title=title)


@app.route('/home/<int:user_id>')
@login_required
def show_tasks(user_id):
    title = "Your List"
    user = User.query.get_or_404(user_id)
    tasks = Task.query.filter_by(author=user).all()
    return render_template("home.html", title=title, tasks=tasks)


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
            flash(f"User {current_user.uname} succesfully logged in", "success")
            return redirect(next_page) if next_page else redirect(url_for("show_tasks", user_id=user.id))
        else:
            flash("Login or password incorrect.", "danger")
    return render_template("login.html", title=title, form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/logout')
def logout():
    logout_user()
    flash("User has been successfully logged out.", "info")
    return redirect(url_for("home"))


@app.route('/task/add', methods=['GET', 'POST'])
@login_required
def add_task():
    title = "Add Task"
    form = AddTaskForm()
    if form.validate_on_submit():
        task = Task(content=form.content.data, author=current_user)
        db.session.add(task)
        db.session.commit()
        flash("Your task has been added!", "success")
        return redirect(url_for("show_tasks", user_id=current_user.id))
    return render_template("addtask.html", title=title, form=form)


@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    title = "Edit Post"
    task = Task.query.get_or_404(task_id)
    form = AddTaskForm()

    if form.validate_on_submit():
        task.content = form.content.data
        db.session.commit()
        flash("Post edited.", "info")
        return redirect(url_for("show_tasks", user_id=current_user.id))
    elif request.method == 'GET':
        form.content.data = task.content
    return render_template("addtask.html", title=title, form=form)


@app.route('/task/<int:task_id>/delete')
@login_required
def delete_task(task_id):
    title = "Delete Post"
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Post deleted.", "info")
    return redirect(url_for("show_tasks", title=title, user_id=current_user.id))


@app.route('/task/<int:task_id>/done')
@login_required
def complete_task(task_id):
    title = "Task Completed"
    task = Task.query.get_or_404(task_id)
    if task.complete is False:
        task.complete = True
        db.session.commit()
    else:
        task.complete = False
        db.session.commit()
    return redirect(url_for("show_tasks", title=title, user_id=current_user.id))


