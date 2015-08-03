""" factory.py """
from flask import Flask

from . import settings
from .extensions import db, security
from .models import User, Role
from .index import bp as index
from .todos import bp as todos

from flask_security import SQLAlchemyUserDatastore
from flask_security.utils import encrypt_password


def create_app(priority_settings=None):
    app = Flask(__name__)

    app.config.from_object(settings)
    app.config.from_envvar('TODO_SETTINGS', silent=True)
    app.config.from_object(priority_settings)

    db.init_app(app)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)

    app.register_blueprint(index)
    app.register_blueprint(todos)

    with app.app_context():
        db.create_all()
        if not User.query.first():
            user_datastore.create_user(
                email='kevin@example.com',
                password=encrypt_password('password'))
            db.session.commit()
    return app
