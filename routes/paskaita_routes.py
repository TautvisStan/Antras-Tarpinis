from flask import render_template
import services.paskaita_actions as pas_act

def init_paskaita_routes(app):
    @app.route('/paskaitos')
    def paskaitos():
        return render_template('paskaitos.html', paskaitos = pas_act.view_paskaitos())

    @app.route('/paskaita_create', methods=['GET', 'POST'])
    def create():
        return