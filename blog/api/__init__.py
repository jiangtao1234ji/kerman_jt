# @Author  :_kerman jt
# @Time    : 19-10-29 下午4:16

from flask import Blueprint, Flask
from flask.helpers import get_env
from flask_cors import CORS

api = Blueprint('api', __name__)


def init_app(app: Flask) -> None:
    from . import views

    app.register_blueprint(api, url_prefix='/api')
    if get_env() == 'development':
        CORS(app, resources={r"/api/*": {"origins": "http://localhost:9527"}}, supports_credentials=True)
