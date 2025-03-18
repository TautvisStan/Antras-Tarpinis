from flask import render_template
import services.grupes_actions as gr_act

def init_grupes_routes(app):
    @app.route('/grupes')
    def moduliai():
        return render_template('grupes.html', moduliai = gr_act.view_grupes())

    @app.route('/grupes_create', methods=['GET', 'POST'])
    def create():
        return