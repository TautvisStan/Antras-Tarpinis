from flask import render_template
import services.modulis_actions as mo_act

def init_modulis_routes(app):
    @app.route('/moduliai')
    def moduliai():
        return render_template('moduliai.html', moduliai = mo_act.view_moduliai())

    @app.route('/moduliai_create', methods=['GET', 'POST'])
    def create():
        return