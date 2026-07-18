# -*- encoding: utf-8 -*-
import os
import time
import logging
from importlib import import_module
from logging.handlers import RotatingFileHandler
from flask import Flask, request, g
from sqlalchemy.exc import IntegrityError
from flask_dance.contrib.google import make_google_blueprint, google

from app.extensions import db, login_manager, migrate, bcrypt, socketio, mail, csrf
from app.utils.authentication.models import User
from app.utils.decorator.time import humanize_date
from app.error_handlers import register_error_handlers

# Détection de l'environnement
IS_VERCEL = os.environ.get("VERCEL") == "1"

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    socketio.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth_blueprint.login"
    login_manager.login_message_category = 'info'

def register_blueprints(app):
    for module_name in ('authentication', 'home', 'admin'):
        module = import_module(f'app.{module_name}.routes')
        app.register_blueprint(module.blueprint)

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def register_custom_filters(app: Flask):
    app.jinja_env.filters['humanize_date'] = humanize_date

def create_app(config="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config)
    
    # Configuration Vercel-friendly
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
    app.config["PROPAGATE_EXCEPTIONS"] = True

    # --- Gestion des fichiers (Uploads) ---
    # N'utilisez que Cloudinary sur Vercel, pas de dossiers locaux
    if not IS_VERCEL:
        UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

    @app.before_request
    def start_timer():
        g.start_time = time.time()

    @app.after_request
    def after_request_handler(response):
        # Logging standard (Vercel le capte automatiquement)
        if hasattr(g, "start_time"):
            duration = round((time.time() - g.start_time) * 1000, 2)
            ip = request.headers.get("X-Forwarded-For", request.remote_addr)
            if ip and "," in ip:
                ip = ip.split(",")[0].strip()
            app.logger.info(f"IP={ip} | {request.method} | {request.full_path} | STATUS={response.status_code} | {duration}ms")

        # Security headers
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    register_extensions(app)
    register_blueprints(app)
    register_custom_filters(app)
    register_error_handlers(app)

    # --- Logs ---
    # Sur Vercel, ne pas créer de fichier local. Les logs vont vers la console.
    if not app.debug and not IS_VERCEL:
        if not os.path.exists("logs"):
            os.makedirs("logs")
        file_handler = RotatingFileHandler("logs/system.log", maxBytes=100*1024*1024, backupCount=10)
        file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        app.logger.addHandler(file_handler)

    # Google OAuth
    google_bp = make_google_blueprint(
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        scope=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"],
        redirect_to="auth_blueprint.google_login"
    )
    app.register_blueprint(google_bp, url_prefix="/authentication")

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app