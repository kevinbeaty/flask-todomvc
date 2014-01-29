""" server.py """
from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request)

import dataset

app = Flask(__name__, static_url_path='')

app.config.from_object('config.default')
app.config.from_envvar('TODO_SETTINGS', silent=True)

db = dataset.connect(app.config['DATABASE'])
todos = db['todos']


@app.route('/')
def index():
    _todos = list(todos.all())
    return render_template('index.html', todos=_todos)


@app.route('/todos/', methods=['POST'])
def todo_create():
    todo = request.get_json()
    todos.insert(todo)
    return _todo_response(todo)


@app.route('/todos/<int:id>')
def todo_read(id):
    todo = _todo_get_or_404(id)
    return _todo_response(todo)


@app.route('/todos/<int:id>', methods=['PUT', 'PATCH'])
def todo_update(id):
    todo = request.get_json()
    todos.update(todo, ['id'])
    return _todo_response(todo)


@app.route('/todos/<int:id>', methods=['DELETE'])
def todo_delete(id):
    todos.delete(id=id)
    return _todo_response({})


def _todo_get_or_404(id):
    todo = todos.find_one(id=id)
    if todo is None:
        abort(404)
    return todo


def _todo_response(todo):
    return jsonify(**todo)


if __name__ == '__main__':
    app.run(port=8000)
