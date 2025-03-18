from flask import Flask, render_template
from config import Config
from extensions import db, migrate, login_manager
from models import atsiskaitymas, grupes, modulis, paskaita, studentai_moduliai, studiju_programa, vartotojas
# from routes import student_routes
from routes import grupes_routes
from routes import login_routes, modulis_routes, studiju_programa_routes
import services.registracija_prisijungimas_actions
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)

# student_routes.init_student_routes(app)
login_routes.init_login_routes(app)
modulis_routes.init_modulis_routes(app)
studiju_programa_routes.init_studiju_programa_routes(app)
grupes_routes.init_grupes_routes(app)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)