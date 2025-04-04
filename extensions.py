from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


class Prisijunges(UserMixin):
    def __init__(self, vaidmuo, studiju_programa_id):
        self.vaidmuo = vaidmuo
        self.studiju_programa_id = studiju_programa_id