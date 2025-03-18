from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()



class Prisijunges(UserMixin):
    def __init__(self, vaidmuo):
        self.vaidmuo = vaidmuo