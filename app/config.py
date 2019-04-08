import os.path
__all__ = ['Config']

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'rest_api.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_VERSION = '0.1'
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/api/'
    OPENAPI_SWAGGER_UI_VERSION = '3.18.3'
    OPENAPI_SWAGGER_UI_PATH = 'swagger'

    SECRET_KEY = os.environ.get('SECRET_KEY', 'something secret')
    JWT_ACCESS_LIFESPAN = {'hours': 24}
    JWT_REFRESH_LIFESPAN = {'days': 30}
