from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Content, Note  # Inclua todos os modelos que você estiver usando
from . import db
import json

# Define o Blueprint
views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    # Busca todos os conteúdos adicionados
    contents = Content.query.all()
    return render_template("home.html", user=current_user, contents=contents)

# Rota para administração de conteúdo, acessível apenas por administradores
@views.route('/admin/content', methods=['GET', 'POST'])
@login_required
def admin_content():
    if not current_user.is_admin:
        flash('Acesso negado: apenas administradores podem acessar esta página.', 'error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        link = request.form.get('link')

        if title and description:
            new_content = Content(title=title, description=description, link=link)
            db.session.add(new_content)
            db.session.commit()
            flash('Conteúdo adicionado com sucesso!', 'success')
            return redirect(url_for('views.admin_content'))
        else:
            flash('Título e descrição são obrigatórios.', 'error')

    contents = Content.query.all()
    return render_template('admin_content.html', contents=contents)
