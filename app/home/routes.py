from app.utils.home import blueprint
from app import db, UPLOAD_FOLDER, csrf, socketio
from flask import render_template, flash, redirect, url_for, jsonify, request
from flask_login import current_user
from sqlalchemy import func


# ---------------------------------------------------------------------------- pour les pages ----------------------------------------------------------------#
# pour la page d'acceuil
@blueprint.route('/')
def home():

    return render_template(
        'home/index.html',
        page_active="home",
    )

# pour la page d'a propos
@blueprint.route('/about')
def about():

    return render_template(
        'home/about.html',
        page_active="about",
    )

# pour la page d'enquete
@blueprint.route('/enquete')
def enquete():

    return render_template(
        'home/enquete.html',
        page_active="enquete",
    )

# pour la page de cours
@blueprint.route('/courses')
def courses():

    return render_template(
        'home/course.html',
        page_active="courses",
    )

# pour la page du blog
@blueprint.route('/blog')
def blog():

    return render_template(
        'home/blog.html',
        page_active="blog",
    )

# pour la page de portfolio
@blueprint.route('/portfolio')
def portfolio():

    return render_template(
        'home/portfolio.html',
        page_active="portfolio",
    )

# pour la page de contact
@blueprint.route('/contact')
def contact():

    return render_template(
        'home/contact.html',
        page_active="contact",
    )

# pour la page d'action
@blueprint.route('/action')
def action():

    return render_template(
        'home/action.html',
        page_active="action",
    )


# ==================================== FORMATIONS =======================================

# pour la page de formation-1
@blueprint.route('/formation_1')
def formation_1():

    return render_template(
        'home/formation-1.html',
        page_active="formation_1",
    )

# pour la page de formation-2
@blueprint.route('/formation_2')
def formation_2():

    return render_template(
        'home/formation-2.html',
        page_active="formation_2",
    )

# pour la page de formation-3
@blueprint.route('/formation_3')
def formation_3():

    return render_template(
        'home/formation-3.html',
        page_active="formation_3",
    )

# pour la page de formation-4
@blueprint.route('/formation_4')
def formation_4():

    return render_template(
        'home/formation-4.html',
        page_active="formation_4",
    )

# pour la page de formation-5
@blueprint.route('/formation_5')
def formation_5():

    return render_template(
        'home/formation-5.html',
        page_active="formation_5",
    )

# pour la page de formation-6
@blueprint.route('/formation_6')
def formation_6():

    return render_template(
        'home/formation-6.html',
        page_active="formation_6",
    )

# ================================== FIN FORMATIONS =====================================



@blueprint.route('/sitemap.xml', methods=['GET'])
def sitemap():
    pages = [
        {'loc': url_for('home', _external=True), 'priority': '1.0'},
        {'loc': url_for('about', _external=True), 'priority': '0.8'},
        {'loc': url_for('enquete', _external=True), 'priority': '0.8'},
        {'loc': url_for('courses', _external=True), 'priority': '0.8'},
        {'loc': url_for('blog', _external=True), 'priority': '0.8'},
        {'loc': url_for('portfolio', _external=True), 'priority': '0.8'},
        {'loc': url_for('contact', _external=True), 'priority': '0.8'},
        {'loc': url_for('action', _external=True), 'priority': '0.8'},
        {'loc': url_for('formation_1', _external=True), 'priority': '0.8'},
        {'loc': url_for('formation_2', _external=True), 'priority': '0.8'},
        {'loc': url_for('formation_3', _external=True), 'priority': '0.8'},
        {'loc': url_for('formation_4', _external=True), 'priority': '0.8'},
        {'loc': url_for('formation_5', _external=True), 'priority': '0.8'},
        {'loc': url_for('formation_6', _external=True), 'priority': '0.8'},
        # ajoute toutes tes pages importantes ici
    ]
    
    xml_sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    for page in pages:
        xml_sitemap.append('<url>')
        xml_sitemap.append(f'<loc>{page["loc"]}</loc>')
        xml_sitemap.append(f'<priority>{page["priority"]}</priority>')
        xml_sitemap.append('</url>')
    
    xml_sitemap.append('</urlset>')
    
    response = Response("\n".join(xml_sitemap), mimetype='application/xml')
    return response