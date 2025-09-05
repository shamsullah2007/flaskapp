from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app = Flask(__name__)


app.config['SECRET_KEY'] = "SHAMSullah098123456sdjkfja@#$%"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydatabase.db"
db = SQLAlchemy(app)
bycrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='logform'
login_manager.login_message_category='info'
from app import routes