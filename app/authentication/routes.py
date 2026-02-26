from app.utils.authentication import blueprint
from app import db, UPLOAD_FOLDER, csrf, socketio
from flask import render_template, flash, redirect, url_for, jsonify, request
from flask_login import current_user
from sqlalchemy import func


# ---------------------------------------------------------------------------- pour les pages ----------------------------------------------------------------#
# pour la page d'acceuil
@blueprint.route('/login')
def login():

    return render_template(
        'authentication/login.html',
        page_active="login",
    )