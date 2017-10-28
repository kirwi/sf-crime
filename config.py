import os

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ('DATABASE_URL')
    DEBUG = False

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Kai@62681@localhost:5432/postgres'
    DEBUG = True
