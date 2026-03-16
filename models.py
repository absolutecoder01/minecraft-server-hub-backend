from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False, default="user")
    servers = db.relationship("Server", backref="owner", lazy=True)


class Server(db.Model):
    __tablename__ = "server"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ip_address = db.Column(db.String)
    version = db.Column(db.String)
    game_mode = db.Column(db.String)
    image_url = db.Column(db.String)
    owner_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)


# Creating decorator admin_required for security reasons


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Get logged user id from jwt token
        #
        # Find user in database using id
        #
        # Check if user.role == admin
        #
        # If admin
        return fn(...)
        # If not
        return 403
