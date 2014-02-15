""" server.py """
from flask import (
    Flask,
    jsonify,
    render_template,
    request)

from flask_sqlalchemy import SQLAlchemy
from flask_security import (
    Security,
    SQLAlchemyUserDatastore,
    UserMixin,
    RoleMixin,
    login_required)
from flask_security.utils import encrypt_password

app = Flask(__name__, static_url_path='')

app.config.from_object('config.default')
app.config.from_envvar('TODO_SETTINGS', silent=True)

db = SQLAlchemy(app)


def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.first():
            user_datastore.create_user(
                email='kevin@example.com',
                password=encrypt_password('password'))
            db.session.commit()


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    order = db.Column(db.Integer)
    completed = db.Column(db.Boolean)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "order": self.order,
            "completed": self.completed}

    def from_json(self, source):
        if 'title' in source:
            self.title = source['title']
        if 'order' in source:
            self.order = source['order']
        if 'completed' in source:
            self.completed = source['completed']

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    active = db.Column(db.Boolean)
    roles = db.relationship(
        'Role', secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


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
