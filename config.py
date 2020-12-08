import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    BUNDLE_ERRORS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    from dotenv import load_dotenv
    load_dotenv()

    ENV = 'development'
    DEBUG = True
    CLIENT_ID = os.environ.get('CLIENT_ID')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MONGO_URI = os.environ.get('MONGO_URI')


class TestingConfig(Config):
    ENV = 'production'
    CLIENT_ID = os.environ.get('CLIENT_ID')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MONGO_URI = os.environ.get('MONGO_URI')


class ProductionConfig(Config):
    ENV = 'production'
    CLIENT_ID = os.environ.get('CLIENT_ID')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MONGO_URI = os.environ.get('MONGO_URI')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
