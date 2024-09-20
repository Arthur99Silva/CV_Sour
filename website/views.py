from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import Content
from . import db

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
        author = request.form.get('author')  # Novo campo de autor
        link = request.form.get('link')

        if title and description and author:
            new_content = Content(title=title, description=description, author=author, link=link)
            db.session.add(new_content)
            db.session.commit()
            flash('Conteúdo adicionado com sucesso!', 'success')
            return redirect(url_for('views.admin_content'))
        else:
            flash('Título, descrição e autor são obrigatórios.', 'error')

    contents = Content.query.all()
    return render_template('admin_content.html', contents=contents)

@views.route('/admin/delete-content/<int:content_id>', methods=['POST'])
@login_required
def delete_content(content_id):
    if not current_user.is_admin:
        flash('Acesso negado: apenas administradores podem deletar conteúdos.', 'error')
        return redirect(url_for('views.admin_content'))

    content = Content.query.get_or_404(content_id)
    db.session.delete(content)
    db.session.commit()
    flash('Conteúdo deletado com sucesso.', 'success')
    return redirect(url_for('views.admin_content'))

# Rota para visualizar o conteúdo específico
@views.route('/content/<int:content_id>')
@login_required
def view_content(content_id):
    content = Content.query.get_or_404(content_id)
    return render_template("view_content.html", content=content)

@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)