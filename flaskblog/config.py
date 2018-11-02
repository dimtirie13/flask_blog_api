import os



class Config:
    SECRET_KEY = '0e8a31259c87a05ec217d1439b50486f'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")
