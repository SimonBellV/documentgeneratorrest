from config import Configuration
from flask import Flask
from .api import api_blueprint as api


app = Flask(__name__)
app.config.from_object(Configuration)
app.register_blueprint(api, url_prefix='/api')
