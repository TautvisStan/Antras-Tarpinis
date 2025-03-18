from flask import render_template
import services.atsiskaitymas_actions as ats_act

def init_atsiskaitymas_routes(app):
    @app.route('/atsiskaitymas')
    def atsiskaitymas():
        return render_template('grupes.html', atsiskaitymas = ats_act.view_atsiskaitymai())

    @app.route('/atsiskaitymas_create', methods=['GET', 'POST'])
    def create():
        return