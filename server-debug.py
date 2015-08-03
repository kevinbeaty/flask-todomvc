from flask_todomvc.factory import create_app
from flask_debugtoolbar import DebugToolbarExtension
from flask_debug_api import DebugAPIExtension

app = create_app()
app.debug = True

# Debug Extensions
DebugToolbarExtension(app)
DebugAPIExtension(app)

# Append Browse API Panel to defaults
config = app.config
panels = list(config['DEBUG_TB_PANELS'])
config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
panels.append('flask_debug_api.BrowseAPIPanel')
config['DEBUG_TB_PANELS'] = panels

# Change API prefix from /api to /todos
config['DEBUG_API_PREFIX'] = '/todos'

app.run(port=8000)
