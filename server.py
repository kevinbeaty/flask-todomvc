""" server.py """
from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request)

TODOS = []

app = Flask(__name__, static_url_path='')
app.debug = True


@app.route('/')
def index():
    todos = filter(None, TODOS)
    return render_template('index.html', todos=todos)


@app.route('/todos/', methods=['POST'])
def todo_create():
    todo = request.get_json()
    todo['id'] = len(TODOS)
    TODOS.append(todo)
    return _todo_response(todo)


@app.route('/todos/<int:id>')
def todo_read(id):
    todo = _todo_get_or_404(id)
    return _todo_response(todo)


@app.route('/todos/<int:id>', methods=['PUT', 'PATCH'])
def todo_update(id):
    todo = _todo_get_or_404(id)
    updates = request.get_json()
    todo.update(updates)
    return _todo_response(todo)


@app.route('/todos/<int:id>', methods=['DELETE'])
def todo_delete(id):
    todo = _todo_get_or_404(id)
    TODOS[id] = None
    return _todo_response(todo)


def _todo_get_or_404(id):
    if not (0 <= id < len(TODOS)):
        abort(404)
    todo = TODOS[id]
    if todo is None:
        abort(404)
    return todo


def _todo_response(todo):
    return jsonify(**todo)


if __name__ == '__main__':
    app.run(port=8000)
