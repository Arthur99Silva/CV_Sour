from website import db
from website.models import User

user = User.query.filter_by(email='arthur9antunes9@gmail.com').first()

if user:
    user.is_admin = True
    db.session.commit()
    print(f'Usuário {user.email} agora é um administrador.')
else:
    print('Usuário não encontrado.')


from website.models import User

users = User.query.all()

for user in users:
    print(f'ID: {user.id}, Email: {user.email}, is_admin: {user.is_admin}')