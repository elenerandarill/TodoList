from myapp import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.uname}','{self.email}')"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"Task('{self.title}','{self.date}')"
