import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'THIS IS A KEY THAT SHOULD BE CHANGED IN PRODUCTION'
    JWT_SECRET_KEY = 'THIS IS ANOTHER KEY THAT SHOULD BE CHANGED IN PRODUCTION'
    SQLALCHEMY_DATABASE_URI = 'postgresql://pizza:pizza@localhost/pizza'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
