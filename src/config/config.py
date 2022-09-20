from decouple import config
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'bushwriters.db')
    RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')
    MAX_IMAGE_FILESIZE = config('MAX_IMAGE_FILESIZE')