from pathlib import Path
import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'a string hard to guess'

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.163.com')
    MAIL_PORT = os.getenv('MAIL_PORT', '25')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASK_MAIL_SUBJECT_PREFIX = '[flask]'
    FLASK_MAIL_SENDER = 'flask Admin <18489969713@163.com>'
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN')

    # SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(Path(__file__).parent / 'data.sqlite')
    SQLALCHEMY_COMMIT_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///{}'.format(Path(__file__).parent / 'data-dev.sqlite')


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,

    'default': DevelopmentConfig
}
