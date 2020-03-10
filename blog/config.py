# @Author  :_kerman jt
# @Time    : 19-10-14 下午7:30


import os
import random
import string

path = os.path.dirname(__file__)


class BaseConfig(object):
    SECRET_KEY = os.getenv("SECRET_KEY", "kerman blog")
    DEFAULT_ADMIN_PASSWORD = "xxxxxx"
    BLOG_PER_PAGE = 10
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    WHOOSHEE_MIN_STRING_LEN = 2
    ADMIN_EMAIL = '1328566866j@gmail.com'
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_DEFAULT_SENDER = os.getenv('FLASK_MAIL_SENDER')
    MAIL_SERVER = os.getenv('FLASK_MAIL_SERVER', 'localhost')
    MAIL_USERNAME = os.getenv('FLASK_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('FLASK_MAIL_PASSWORD')
    GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    # SQLALCHEMY_DATABASE_URI = os.getenv(
    #     "DATABASE_URL", "sqlite:///" + os.path.join(path, "db.sqlite3")
    # )


class ProductionConfig(BaseConfig):
    # if "DATABASE_URL" in os.environ.keys():
    #     print(11111111111111111)

    if "DATABASE_URL" in os.environ:
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "")
        # print(SQLALCHEMY_DATABASE_URI)
    else:
        SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:xxxxxxx@localhost/xxx?charset=utf8"


class DevelopConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:xxxxxxxx@localhost/xxxx?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    TESTING = True


config_dict = {
    "production": ProductionConfig,
    "development": DevelopConfig,
    "testing": TestingConfig,
}
