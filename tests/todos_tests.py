import unittest
import json

from . import settings
from flask_todomvc.extensions import db
from flask_todomvc.factory import create_app


class TodoTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(
            priority_settings=settings)
        self.client = self.app.test_client()
        self.order = 1

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def create(self, title, completed=False):
        todo = {"title": title,
                "order": self.order,
                "completed": completed}
        response = self.client.post(
            '/todos/',
            data=json.dumps(todo),
            content_type='application/json')
        created = json.loads(response.data)

        assert 'id' in created
        assert created['title'] == title
        assert created['order'] == self.order
        assert created['completed'] == completed
        self.order += 1

        return created

    def read(self, id):
        response = self.client.get(
            '/todos/%d' % id,
            content_type='application/json')
        if response.status_code != 200:
            assert response.status_code == 404
            return None
        return json.loads(response.data)

    def test_config_settings(self):
        config = self.app.config
        assert config['SQLALCHEMY_DATABASE_URI'] == \
            'sqlite:///test.db'
        assert config['TESTING']
        assert config['DEBUG']

    def test_create(self):
        todo1 = self.create('Pick up kids')
        assert todo1['title'] == 'Pick up kids'
        assert todo1['order'] == 1
        assert not todo1['completed']

        todo2 = self.create(
            'Buy groceries', completed=True)
        assert todo2['title'] == 'Buy groceries'
        assert todo2['order'] == 2
        assert todo2['completed']

        assert todo1['id'] != todo2['id']

    def test_read(self):
        todo1 = self.create('Pick up kids')
        todo2 = self.create(
            'Buy groceries', completed=True)

        read1 = self.read(todo1['id'])
        read2 = self.read(todo2['id'])

        assert read1 == todo1
        assert read2 == todo2

        read3 = self.read(todo2['id'] + 1)
        assert read3 is None

    def test_update(self):
        todo = self.create('Pick up kids')
        id = todo['id']

        updates = dict(**todo)
        updates['completed'] = True
        updates['title'] = 'Pick up *all* kids'

        req = self.client.put(
            '/todos/%d' % id,
            data=json.dumps(updates),
            content_type='application/json')
        updated = json.loads(req.data)

        assert updated == updates
        assert self.read(id) == updates

    def test_delete(self):
        todo = self.create('Pick up kids')
        id = todo['id']
        assert self.read(id) == todo

        self.client.delete(
            '/todos/%d' % id)

        assert self.read(id) is None
