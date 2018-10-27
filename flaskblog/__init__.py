from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '0e8a31259c87a05ec217d1439b50486f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# database instance
db = SQLAlchemy(app)

from flaskblog import routes
