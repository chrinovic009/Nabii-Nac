from app.extensions import db, bcrypt
from flask_login import UserMixin
from datetime import datetime

# ======================================================= TABLES DES DONNEES ============================================================ #

# Modèle utilisateur
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255))
    family_name = db.Column(db.String(255))

    password_hash = db.Column(db.String(255), nullable=True)

    auth_provider = db.Column(
        db.Enum("local", "google", "apple", name="auth_provider"),
        default="local",
        nullable=False
    )

    google_id = db.Column(db.String(64), unique=True, nullable=True)

    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# pour les erreurs de l'application
class SystemErrorLog(db.Model):
    __tablename__ = "system_error_logs"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    error_type = db.Column(
        db.Enum(
            "application",
            "database",
            "external_api",
            "timeout",
            name="system_error_type"
        ),
        nullable=False
    )

    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User")


