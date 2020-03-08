import os

basedir = os.path.abspath(os.path.dirname(__file__))


class ConfigBase(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
