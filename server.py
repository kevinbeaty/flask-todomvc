""" server.py """

from flask_todomvc.factory import create_app
app = create_app()
app.run(port=8000)

import psycopg2

conn = psycopg2.connect(
    "replace this string with connection details, include a password='something' field"
)

conn = psycopg2.connect("dbname=test user=postgres password='thisisapassword!#@'")

print("ye")
