""" server.py """
from flask import (
    Flask,
    jsonify,
    render_template,
    request)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='')

app.config.from_object('config.default')
app.config.from_envvar('TODO_SETTINGS', silent=True)

db = SQLAlchemy(app)


def init_db():
    db.create_all()


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


@app.route('/')
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
