from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_datepicker import datepicker

from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()

bcrypt = Bcrypt()
datepicker = datepicker()

login_manager = LoginManager()
login_manager.login_view = 'auth_blueprint.user_login'
login_manager.login_message_category = 'info'

db_url = 'localhost:5432'
db_name = 'ojce-projects'
db_user = 'postgres'
db_password = 'jefF1234'
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}')
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Entity():
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    last_updated_by = Column(Integer)

    def __init__(self, created_by):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_updated_by = created_by