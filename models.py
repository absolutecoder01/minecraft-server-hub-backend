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
    status = db.Column(db.String, nullable=False, default="online")
    servers = db.relationship("Server", backref="owner", lazy=True)


class Server(db.Model):
    __tablename__ = "server"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ip_address = db.Column(db.String, nullable=False)
    version = db.Column(db.String, nullable=False)
    game_mode = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)


# Creating decorator admin_required for security reasons
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Get logged user id from jwt token
        current_user_identity = get_jwt_identity()
        user = User.query.filter_by(username=current_user_identity).first()
        if user and user.role == "admin":
            return fn(*args, **kwargs)
        else:
            return jsonify({"error": "Admin access required!"}), 403

    return wrapper
