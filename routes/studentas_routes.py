from flask import render_template
from flask_login import login_required, current_user

def init_studentas_routes(app):
    @app.route('/studentas/profilis')
    @login_required
    def studento_profilis():
        if current_user.vaidmuo != 'Studentas':
            return "Tik studentai gali perziurėti savo profilį", 403

        studentas = current_user
        moduliai = studentas.moduliai
        grupe = studentas.grupe
        studiju_programa = studentas.studiju_programa
        fakultetas = studentas.fakultetas

        return render_template('studentas_profilis.html',studentas=studentas,moduliai=moduliai,grupe=grupe,studiju_programa=studiju_programa,fakultetas=fakultetas)