from apos.config_base import ConfigBase


class Config(ConfigBase):
    SECRET_KEY = 'THIS IS A KEY THAT SHOULD BE CHANGED IN PRODUCTION'
    JWT_SECRET_KEY = 'THIS IS ANOTHER KEY THAT SHOULD BE CHANGED IN PRODUCTION'
    SQLALCHEMY_DATABASE_URI = 'postgresql://pizza:pizza@localhost/pizza'
