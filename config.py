"""
DON'T FORGET TO NAME YOUR DATABASES when you come to use!
THEN, before running anything remember to physically create database using pgAdmin.

Shortly after we will apply db initialisation, modelling and data population.
See db_create_migrate for more.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
import os
from config_templates import *
from config_vars import PK, DBNAME
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


# ====================
# 1. CONFIG CLASSES
# ====================
class Config(TemplateParameters):
    """
    Sets Encryption, and your database addresses.
    """
    # Used to sign cookies (careful if change the string/label when moving to production)
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))
    # For form protection
    WTF_CSRF_ENABLED = True
    ## WTF_CSRF_SECRET_KEY = SECRET_KEY
    DEVEL_DATABASE_NAME = 'postgresql+psycopg2://postgres:{0}@localhost:{1}/Backup_{2}'.\
        format(PK[0], PK[1], DBNAME)
    PROD_DATABASE_NAME = 'postgresql+psycopg2://postgres:{0}@localhost:{1}/Backup_{2}'.\
        format(PK[0], PK[1], DBNAME)

    @staticmethod
    def init_app(app):
        pass


class DevelConfig(Config):
    """
    Settings for development database.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', Config.DEVEL_DATABASE_NAME)


class ProdConfig(Config):
    """
    Settings for production database.
    """
    DEBUG = False
    PRODUCT = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', Config.PROD_DATABASE_NAME)


config = {
    'development': DevelConfig,
    'production': ProdConfig,
    'default': DevelConfig
}


# ====================
# 2. CONFIG OUR SCHEDULER
# ====================
def kickstart_scheduler(scheduler, config_name):
    """
    simple call to jobstore;
    add any other features that you wish.
    """
    jobstores = {
        'sqlalchemy': SQLAlchemyJobStore(
            url=config[config_name].SQLALCHEMY_DATABASE_URI)
    }
    scheduler.configure(jobstores=jobstores)
    scheduler.start()


# =====================================
if __name__ == '__main__':
    print config['development'].DEBUG
    print Config.DEVEL_DATABASE_NAME
