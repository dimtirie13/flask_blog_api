from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '0e8a31259c87a05ec217d1439b50486f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# allows users to only access account page after log in/ redirect if not logged in
login_manager.login_view = 'login'
# nice log In message with bootstrap
login_manager.login_message_category = 'info'


from flaskblog import routes
