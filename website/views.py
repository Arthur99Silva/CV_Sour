from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Content, Note  # Inclua todos os modelos que você estiver usando
from . import db
import json

# Define o Blueprint
views = Blueprint('views', __name__)

# Rota para a página inicial
@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

# Rota para adicionar notas (presumindo que você tinha uma funcionalidade assim)
@views.route('/add-note', methods=['POST'])
@login_required
def add_note():
    note = request.form.get('note')

    if len(note) < 1:
        flash('Note is too short!', category='error')
    else:
        new_note = Note(data=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Note added!', category='success')

    return redirect(url_for('views.home'))

# Rota para deletar notas
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted!', category='success')

    return jsonify({})

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
