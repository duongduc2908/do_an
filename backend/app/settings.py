import os
os_env = os.environ


class Config(object):
    SECRET_KEY = '3nF3Rn0'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class ProdConfig(Config):
    """Production configuration."""
    # app config
    ENV = 'prod'
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    HOST = '0.0.0.0'
    TEMPLATES_AUTO_RELOAD = False
    # Celery background task config
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_BACKEND_URL = 'redis://localhost:6379'
    # JWT Config
    JWT_SECRET_KEY = '1234567a@'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    # MongoDB config
    MONGO_DBNAME = 'cham_cong'
    MONGO_URI = 'mongodb://127.0.0.1:27017/cham_cong'
    MONGO_AUTH_SOURCE = ''
    MONGO_USERNAME = ''
    MONGO_PASSWORD = ''
    MONGO_CONNECT = False
    CONNECT = False
    # REDIS
    SLACK_WEBHOOK = "https://hooks.slack.com/services/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"



class DevConfig(Config):
    """Development configuration."""
    # app config
    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_ENABLED = True  # Disable Debug toolbar
    TEMPLATES_AUTO_RELOAD = True
    HOST = '0.0.0.0'
    # Celery background task config
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_BACKEND_URL = 'redis://localhost:6379'
    # JWT Config
    JWT_SECRET_KEY = '1234567a@@'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    # MongoDB config
    MONGO_DBNAME = 'cham_cong'
    MONGO_URI = 'mongodb://127.0.0.1:27017/cham_cong'
    MONGO_AUTH_SOURCE = ''
    MONGO_USERNAME = ''
    MONGO_PASSWORD = ''
    MONGO_CONNECT = False
    CONNECT = False
    # REDIS
    REDIS_URL = "redis://localhost:6379"

