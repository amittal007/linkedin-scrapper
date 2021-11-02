from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from selenium import webdriver
from linkedin_scraper import Company, actions
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3308/linkedin'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

email = "kit.rishabh7530@gmail.com"
password = "@a818027530"
# driver = webdriver.Chrome()
# actions.login(driver, email, password)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'login'

from app import main