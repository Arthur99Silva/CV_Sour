from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Substitua por uma chave segura
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Importa as rotas (blueprints)
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Modelos (para garantir que as tabelas sejam criadas)
    from .models import User, Content

    with app.app_context():
        db.create_all()

    # Configuração do Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Carrega o usuário a partir do ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Injeta 'current_user' em todos os templates como 'user'
    @app.context_processor
    def inject_user():
        return dict(user=current_user)

    return app
