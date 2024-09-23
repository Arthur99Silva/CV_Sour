from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                # Redireciona para a home com uma mensagem de sucesso
                return redirect(url_for('views.home', success_message="Login efetuado com sucesso!"))
            else:
                return render_template('login.html', error_message="Senha incorreta, tente novamente.")
        else:
            return render_template('login.html', error_message="Usuário não encontrado.")

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()

        if user:
            return render_template('sign_up.html', error_message="Email já cadastrado.")
        elif len(password1) < 7:
            return render_template('sign_up.html', error_message="A senha deve ter pelo menos 7 caracteres.")
        elif password1 != password2:
            return render_template('sign_up.html', error_message="As senhas não coincidem.")
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('views.home'))

    return render_template('sign_up.html')