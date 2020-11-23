import os


class Config(object):  # 所有配置类的父类，通用的配置写在这里
    SECRET_KEY = 'Secret Key!'


class DevelopmentConfig(Config):  # 开发环境配置类
    ENV = 'development'
    DEBUG = True
    CLIENT_ID = "422430406019-4knnkh10lgpftp3a7hhi3cd17ljdnat2.apps.googleusercontent.com"
    SQLALCHEMY_DATABASE_URI = 'postgresql://192.168.1.105/flowpoint'

    MONGO_URI = 'mongodb://192.168.1.105:27017/flowpoint?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false'

    BUNDLE_ERRORS = True

class TestingConfig(Config):  # 测试环境配置类
    pass


class ProductionConfig(Config):  # 生产环境配置类
    ENV = 'production'
    CLIENT_ID = "422430406019-4knnkh10lgpftp3a7hhi3cd17ljdnat2.apps.googleusercontent.com"

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:sw137982@database-1.cjeimtpjlvpf.ap-northeast-1.rds.amazonaws.com/postgres'
    MONGO_URI = 'mongodb://admin:sw137982@18.181.85.231:27017/block_styles?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false'
    BUNDLE_ERRORS = True


config = {  # config字典注册了不同的配置，默认配置为开发环境，本例使用开发环境
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
