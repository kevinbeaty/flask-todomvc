""" server.py """

from flask_todomvc.factory import create_app
app = create_app()
app.run(port=8000)
