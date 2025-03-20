from flask import render_template
from extensions import db
from services.administratorius_actions import gauti_statistika


def init_administratorius_routes(app):
    @app.route('/statistika')
    def atvaizduoti_statistika():
        vartotoju_skaicius,moduliu_skaicius,studiju_programu_skaicius,grupiu_skaicius = gauti_statistika()
        
        return render_template('statistika.html', vartotoju_skaicius = vartotoju_skaicius, moduliu_skaicius = moduliu_skaicius, studiju_programu_skaicius = studiju_programu_skaicius,grupiu_skaicius = grupiu_skaicius)