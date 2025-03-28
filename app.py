from flask import Flask, render_template
from config import Config
from extensions import db, migrate, login_manager, mail
from flask_login import LoginManager
import pymysql
pymysql.install_as_MySQLdb()  # Svarbu: turi būti prieš SQLAlchemy inicijavimą!


# from models import models
from models.vartotojas import Vartotojas
from models.modulis import Modulis
from models.paskaita import Paskaita
from models.atsiskaitymas import Atsiskaitymas
from models.studiju_programa import StudijuPrograma
from models.grupes import Grupe
from models.kalendorius import Kalendorius
from models.studento_pasiekimai import StudentoPasiekimai
from models.studentai_moduliai import StudentasModulis
from models.uzduotis import Uzduotis
from models.fakultetas import Fakultetas


# from routes import routes
from routes import grupes_routes
from routes import login_routes, modulis_routes, studiju_programa_routes, admin_routes
from routes.paveiksleliu_routes import inicijuoti_marsrutus
from routes.paskaita_routes import init_paskaita_routes
# from routes.atsiskaitymas_routes import init_atsiskaitymas_routes
from routes.studentai_moduliai_routes import init_studento_moduliu_routes
from routes.studento_pasiekimai_routes import init_studento_pasiekimas_routes
from routes.vartotojas_routes import init_vartotojas_routes
from routes.login_routes import init_login_routes
from routes.testas_route import init_testas
from routes.studentas_routes import init_studentas_routes

import services.registracija_prisijungimas_actions

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)
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
# init_atsiskaitymas_routes(app)
init_vartotojas_routes(app)
init_testas(app)
init_studentas_routes(app)
init_studento_pasiekimas_routes(app)

init_studento_moduliu_routes(app)

login_routes.init_login_routes(app)
modulis_routes.init_modulis_routes(app)
studiju_programa_routes.init_studiju_programa_routes(app)
grupes_routes.init_grupes_routes(app)
# vartotojas_routes.init_vartotojas_routes(app)
admin_routes.init_admin_routes(app)

# profilio foto
inicijuoti_marsrutus(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)