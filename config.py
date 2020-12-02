import os


class Config(object):
    SECRET_KEY = 'Secret Key!'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    CLIENT_ID = "422430406019-4knnkh10lgpftp3a7hhi3cd17ljdnat2.apps.googleusercontent.com"
    SQLALCHEMY_DATABASE_URI = 'postgresql://192.168.1.105/flowpoint'

    MONGO_URI = 'mongodb://192.168.1.105:27017/flowpoint?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false'

    BUNDLE_ERRORS = True


class TestingConfig(Config):
    ENV = 'production'
    CLIENT_ID = os.environ.get('CLIENT_ID')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MONGO_URI = os.environ.get('MONGO_URI')
    BUNDLE_ERRORS = True


class ProductionConfig(Config):
    ENV = 'production'
    CLIENT_ID = os.environ.get('CLIENT_ID')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MONGO_URI = os.environ.get('MONGO_URI')
    BUNDLE_ERRORS = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
