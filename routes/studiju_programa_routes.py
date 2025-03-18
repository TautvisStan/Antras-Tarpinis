from flask import render_template
import services.studiju_programa_actions as spr_act

def init_studiju_programa_routes(app):
    @app.route('/studiju_programa')
    def studiju_programa():
        return render_template('studiju_programa.html', studiju_programa = spr_act.view_studiju_programa())

    @app.route('/studiju_programa_create', methods=['GET', 'POST'])
    def create():
        return