from flask import Flask, render_template
from config import Config
from extensions import db, migrate, login_manager, mail
from flask_login import LoginManager
from models import studentai_moduliai

# from models import models
from models.vartotojas import Vartotojas
from models.modulis import Modulis
from models.paskaita import Paskaita
from models.atsiskaitymas import Atsiskaitymas
from models.studiju_programa import StudijuPrograma
from models.grupes import Grupe
from models.kalendorius import Kalendorius

# from routes import routes
from routes import grupes_routes
from routes import login_routes, modulis_routes, studiju_programa_routes, vartotojas_routes, administratorius_routes
from routes.paveiksleliu_routes import inicijuoti_marsrutus
from routes.paskaita_routes import init_paskaita_routes
from routes.atsiskaitymas_routes import init_atsiskaitymas_routes
from routes.vartotojas_routes import init_vartotojas_routes
from routes.login_routes import init_login_routes

import services.registracija_prisijungimas_actions

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
mail.init_app(app)

# Flask-Login inicializacija
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_routes.login'

@login_manager.user_loader
def load_user(user_id):
    from models.vartotojas import Vartotojas
    return db.session.get(Vartotojas, int(user_id))

# Importuojame maršrutus
init_paskaita_routes(app)
init_atsiskaitymas_routes(app)
init_vartotojas_routes(app)
init_login_routes(app)

login_routes.init_login_routes(app)
modulis_routes.init_modulis_routes(app)
studiju_programa_routes.init_studiju_programa_routes(app)
grupes_routes.init_grupes_routes(app)
vartotojas_routes.init_student_routes(app)
administratorius_routes.init_administratorius_routes(app)

# profilio foto
inicijuoti_marsrutus(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)