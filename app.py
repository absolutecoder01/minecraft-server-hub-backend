# Here will be Routes, Config, Models all together
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from flask_sqlalchemy import SQLAlchemy

from models import db

load_dotenv()
from utils import hash_password, verify_password


def create_app():
    app = Flask(__name__)

    # Konfiguracja
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    # Inicjalizacja
    db.init_app(app)
    CORS(app)
    jwt = JWTManager(app)

    # --- ROUTES ---
    @app.route("/")
    def home():
        return "<p>Hello, World!</p>"

    # User management
    # Accepts username, password, role. Logic: Check if user exists, hash password, save to DB.
    @app.route("/api/auth/register", methods=["POST"])
    def register():
        pass

    # Accepts username, password. Logic: Verify password, return a JWT token.
    @app.route("/api/auth/login")
    def login():
        pass

    # Server management
    # Returns a list of all servers. Logic: Query DB, return JSON array.
    @app.route("/api/servers")
    def servers():
        pass

    # Details of one server.
    @app.route("/api/servers/<int:server_id>")
    def server_details():
        pass

    # Create a server. Logic: Check if user is logged in via JWT. Save owner_id as the current user's ID.
    @app.route("/api/servers")
    def create_server():
        pass

    # Delete a server. Crucial Logic: Check if the requester is the owner_id OR if the requester has the admin role. If neither, return 403 Forbidden.
    @app.route("/api/servers/<int:server_id>")
    def delete_server():
        pass

    # Edit a server. Logic: Same permission check as delete, but only Admins can edit servers they don't own.
    @app.route("/api/servers/<int:server_id>")
    def edit_server():
        pass

    # Returns data for charts (e.g., total users, total servers, servers per game mode). Logic: Perform SQL aggregations (COUNT, GROUP BY).
    @app.route("/api/admin/stats")
    def admin_stats():
        pass

    return app


if "__main__" == __name__:
    app = create_app()
    app.debug = True
    with app.app_context():
        from models import Server, User

        db.create_all()
    app.run()
