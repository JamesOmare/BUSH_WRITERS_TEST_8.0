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
    MAIL_SERVER = config('MAIL_SERVER')
    MAIL_PORT = config('MAIL_PORT')
    MAIL_USE_SSL = config('MAIL_USE_SSL')
    MAIL_USERNAME = config('MAIL_USERNAME')
    MAIL_PASSWORD = config('MAIL_PASSWORD')

    # Fluid layout True or False
    FLASK_ADMIN_FLUID_LAYOUT = True

    # Set the theme name
    FLASK_ADMIN_SWATCH = 'flatly'

    #paypal
    PAYPAL_BUSINESS_CLIENT_ID = config('PAYPAL_BUSINESS_CLIENT_ID')
    PAYPAL_BUSINESS_SECRET = config('PAYPAL_BUSINESS_SECRET')
    PAYPAL_API_URL = config('PAYPAL_API_URL')
    IB_TAX_APP_PRICE = config('IB_TAX_APP_PRICE')
    IB_TAX_APP_PRICE_CURRENCY = config('IB_TAX_APP_PRICE_CURRENCY')

    # mpesa
    CONSUMER_KEY = config('CONSUMER_KEY')
    CONSUMER_SECRET = config('CONSUMER_SECRET')