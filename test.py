from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Путь к вашей базе данных SQLite
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    tagId = db.Column(db.Integer)


# Создаем базу данных, если она еще не существует
# db.create_all()

@app.route('/', methods=['GET'])
def index():
    search_query = request.args.get('search', '')  # Получаем значение параметра 'search' из URL
    page = request.args.get('page', 1, type=int)  # Получаем значение параметра 'page' из URL

    # Формируем запрос для поиска пользователей по name, email и phone
    query = User.query.filter(User.name.contains(search_query) |
                              User.email.contains(search_query) |
                              User.phone.contains(search_query) &
                              (User.group == 2))

    # Выполняем пагинацию по 10 записей на страницу
    all_users = query.paginate(page=page, per_page=10)

    return render_template('index.html', users=users, search_query=search_query)


if __name__ == '__main__':
    app.run()
