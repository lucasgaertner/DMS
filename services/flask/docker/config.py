import os

#user = os.environ['POSTGRES_USER']
#password = os.environ['POSTGRES_PASSWORD']
#host = os.environ['POSTGRES_HOST']
#database = os.environ['POSTGRES_DB']
#port = os.environ['POSTGRES_PORT'
#
#DATABASE_CONNCECTION_URI = f'postgresql://{user}:{password}@{host}:{port}/{database}'


DBUSER = 'postgres'
DBPASS = 'start.123'
DBHOST = 'postgres'
DBPORT = '5432'
DBNAME = 'documents'

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '123456789'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(user=DBUSER,passwd=DBPASS,host=DBHOST,port=DBPORT,db=DBNAME)
	SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True