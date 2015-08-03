from flask_todomvc.factory import create_app
app = create_app()
app.debug = True

from flask_debugtoolbar import DebugToolbarExtension
DebugToolbarExtension(app)

app.run(port=8000)
