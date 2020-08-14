import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI='postgresql://postgres:root@localhost:5432/castingagency'
SQLALCHEMY_TRACK_MODIFICATIONS=False
# class Config(object):
#     """Add configuration variables."""
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
