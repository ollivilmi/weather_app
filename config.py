import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
	DEBUG = False
	SECRET_KEY = '\x10@\x8b\xf5\xfeQw\x89\xca\xe8\x0fb\x8d\xe78\x1e\x83\x8696\x04\xf1@'
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_ECHO = True

class DevelopmentConfig(BaseConfig):
	DEBUG = True
	
class ProductionConfig(BaseConfig):
	DEBUG = False