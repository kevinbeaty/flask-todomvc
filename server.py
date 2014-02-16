""" server.py """
from flask import (
    Flask,
    jsonify,
    render_template,
    request)

from flask_todomvc import settings
from flask_todomvc.extensions import db, security
from flask_todomvc.models import User, Role, Todo

from flask_security import (
    SQLAlchemyUserDatastore,
    login_required)
from flask_security.utils import encrypt_password

app = Flask(__name__, static_url_path='')

app.config.from_object(settings)
app.config.from_envvar('TODO_SETTINGS', silent=True)

db.init_app(app)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security.init_app(app, user_datastore)


def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.first():
            user_datastore.create_user(
                email='kevin@example.com',
                password=encrypt_password('password'))
            db.session.commit()


@app.route('/')
@login_required
def index():
    todos = Todo.query.all()
    todo_list = map(Todo.to_json, todos)
    return render_template(
        'index.html', todos=todo_list)


@app.route('/todos/', methods=['POST'])
def todo_create():
    todo = Todo()
    todo.from_json(request.get_json())
    db.session.add(todo)
    db.session.commit()
    return _todo_response(todo)


@app.route('/todos/<int:id>')
def todo_read(id):
    todo = Todo.query.get_or_404(id)
    return _todo_response(todo)


@app.route('/todos/<int:id>', methods=['PUT', 'PATCH'])
def todo_update(id):
    todo = Todo.query.get_or_404(id)
    todo.from_json(request.get_json())
    db.session.commit()
    return _todo_response(todo)


@app.route('/todos/<int:id>', methods=['DELETE'])
def todo_delete(id):
    Todo.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify()


def _todo_response(todo):
    return jsonify(**todo.to_json())


if __name__ == '__main__':
    init_db()
    app.run(port=8000)
