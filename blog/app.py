# @Author  :_kerman jt
# @Time    : 19-10-14 下午2:30

from typing import Union, Optional
from flask import Flask, request, g
from flask.helpers import get_env
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext
from flask_assets import Environment
from flask_login import LoginManager
# from dotenv import load_dotenv

from . import STATIC_PATH, config, models, cli, views, admin, templating, api
from .models import User, Blog, Tag, Category, Integration, Comment, Page

from .md import markdown


def create_app(env: Optional[str] = None) -> Flask:
    # load_dotenv('.env')
    env = env or get_env()
    app = Flask(__name__, static_folder=STATIC_PATH)
    app.config.from_object(config.config_dict[env])
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    Moment(app)
    babel = Babel(app)
    models.init_app(app)
    cli.init_app(app)
    views.init_app(app)
    if env == "development":
        admin.init_app(app)
    templating.init_app(app)
    api.init_app(app)
    Environment(app)

    @babel.localeselector
    def get_locale():
        lang = request.accept_languages.best_match(['zh', 'en'])
        if not lang and 'site' in g:
            lang = g.site['locale']
        if lang == 'zh':
            lang = 'zh_Hans_CN'
        return lang

    login_manager = LoginManager(app)
    login_manager.login_view = "admin.login"
    login_manager.login_message = lazy_gettext('Please login')
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def get_user(uid):
        return models.User.query.get(uid)

    @app.shell_context_processor
    def shell_context():
        return {'db': models.db, 'Blog': models.Blog, 'markdown': markdown}

    return app
