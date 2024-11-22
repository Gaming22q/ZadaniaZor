from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_testing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для пользователей
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Модель для тестов
class Test(db.Model):
    test_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

# Модель для результатов тестов
class Result(db.Model):
    result_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    test_id = db.Column(db.Integer, db.ForeignKey('test.test_id'))
    score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Создание базы данных
@app.before_first_request
def create_tables():
    db.create_all()

# API для управления тестами
@app.route('/tests', methods=['POST'])
def add_test():
    """
    Создать новый тест.
    Запрос: { "title": "Тест на профориентацию", "description": "Описание теста" }
    Ответ: { "message": "Test created" }
    """
    data = request.json
    new_test = Test(title=data['title'], description=data['description'])
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

# API для прохождения тестов и сохранения результатов
@app.route('/results', methods=['POST'])
def save_result():
    """
    Сохранить результат теста.
    Запрос: { "user_id": 1, "test_id": 1, "score": 85.0 }
    Ответ: { "message": "Result saved" }
    """
    data = request.json
    new_result = Result(user_id=data['user_id'], test_id=data['test_id'], score=data['score'])
    db.session.add(new_result)
    db.session.commit()
    return jsonify({'message': 'Result saved'}), 201

@app.route('/results/<int:user_id>', methods=['GET'])
def get_results(user_id):
    """
    Получить результаты тестов для пользователя.
    Ответ: [{ "result_id": 1, "test_id": 1, "score": 85.0, "created_at": "2023-10-01 12:00:00" }, ...]
    """
    results = Result.query.filter_by(user_id=user_id).all()
    return jsonify([{'result_id': result.result_id, 'test_id': result.test_id, 'score': result.score, 'created_at': result.created_at} for result in results]), 200

if __name__ == '__main__':
    app.run(debug=True)
