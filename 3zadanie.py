from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_testing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для пользователей
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор пользователя
    email = db.Column(db.String(255), unique=True, nullable=False)  # Электронная почта пользователя
    password = db.Column(db.String(255), nullable=False)  # Пароль пользователя

# Модель для тестов
class Test(db.Model):
    test_id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор теста
    title = db.Column(db.String(255), nullable=False)  # Название теста
    description = db.Column(db.Text, nullable=True)  # Описание теста
    created_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))  # Идентификатор создателя теста

# Создание базы данных
@app.before_first_request
def create_tables():
    db.create_all()

# API для управления пользователями
@app.route('/users', methods=['POST'])
def add_user():
    """
    Создать нового пользователя.
    Запрос: { "email": "user@example.com", "password": "password123" }
    Ответ: { "message": "User created" }
    """
    data = request.json
    new_user = User(email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

@app.route('/users', methods=['GET'])
def get_users():
    """
    Получить список всех пользователей.
    Ответ: [{ "user_id": 1, "email": "user@example.com" }, ...]
    """
    users = User.query.all()
    return jsonify([{'user_id': user.user_id, 'email': user.email} for user in users]), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Обновить информацию о пользователе по его идентификатору.
    Запрос: { "email": "new_email@example.com", "password": "new_password123" }
    Ответ: { "message": "User updated" } или { "message": "User not found" }
    """
    data = request.json
    user = User.query.get(user_id)
    if user:
        user.email = data['email']
        user.password = data['password']
        db.session.commit()
        return jsonify({'message': 'User updated'}), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Удалить пользователя по его идентификатору.
    Ответ: { "message": "User deleted" } или { "message": "User not found" }
    """
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'}), 200
    return jsonify({'message': 'User not found'}), 404

# API для управления тестами
@app.route('/tests', methods=['POST'])
def add_test():
    """
    Создать новый тест.
    Запрос: { "title": "Тест на профориентацию", "description": "Описание теста", "created_by": 1 }
    Ответ: { "message": "Test created" }
    """
    data = request.json
    new_test = Test(title=data['title'], description=data['description'], created_by=data['created_by'])
    db.session.add(new_test)
    db.session.commit()
    return jsonify({'message': 'Test created'}), 201

@app.route('/tests', methods=['GET'])
def get_tests():
    """
    Получить список всех тестов.
    Ответ: [{ "test_id": 1, "title": "Тест на профориентацию", "description": "Описание теста" }, ...]
    """
    tests = Test.query.all()
    return jsonify([{'test_id': test.test_id, 'title': test.title, 'description': test.description} for test in tests]), 200

@app.route('/tests/<int:test_id>', methods=['PUT'])
def update_test(test_id):
    """
    Обновить тест по его идентификатору.
    Запрос: { "title": "Новое название", "description": "Новое описание" }
    Ответ: { "message": "Test updated" } или { "message": "Test not found" }
    """
    data = request.json
    test = Test.query.get(test_id)
    if test:
        test.title = data['title']
        test.description = data['description']
        db.session.commit()
        return jsonify({'message': 'Test updated'}), 200
    return jsonify({'message': 'Test not found'}), 404

@app.route('/tests/<int:test_id>', methods=['DELETE'])
def delete_test(test_id):
    """
    Удалить тест по его идентификатору.
    Ответ: { "message": "Test deleted" } или { "message": "Test not found" }
    """
    test = Test.query.get(test_id)
    if test:
        db.session.delete(test)
        db.session.commit()
        return jsonify({'message': 'Test deleted'}), 200
    return jsonify({'message': 'Test not found'}), 404

if __Test__ == '__main__':
    app.run(debug=True)
