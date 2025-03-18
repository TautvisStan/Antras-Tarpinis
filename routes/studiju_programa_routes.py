from flask import flash, render_template, request, url_for
import services.studiju_programa_actions as sp_act
from forms.studijuProgramaForma import StudijuProgramaForma
def init_modulis_routes(app):
    @app.route('/studiju_programos')
    def studiju_programos():
        return render_template('studiju_programos.html', studiju_programos = sp_act.view_studiju_programa())

    @app.route('/studiju_programos_create', methods=['GET', 'POST'])
    def st_pr_create():
        form = StudijuProgramaForma()
        if request.method == 'GET':
            return render_template("studiju_programos_forma.html", form=form)
        else:    
            try:
                pavadinimas = form.pavadinimas.data
                sp_act.sukurti_studiju_programa(pavadinimas)
                flash("Sekmingai sukurta")
                return app.redirect(url_for('studiju_programos'), 302)
            except Exception as e:
                zinute = e
            return render_template("studiju_programos_forma.html", form=form)  
    
    @app.route('/studiju_programos_update/<id>', methods=['GET', 'POST'])
    def st_pr_update(id):
        studiju_programa = sp_act.gauti_studiju_programa(id)
        form = StudijuProgramaForma(obj=studiju_programa)
        if request.method == 'GET':
            return render_template("studiju_programos_forma_update.html", form=form, id=id)
        else:    
            try:
                pavadinimas = form.pavadinimas.data
                sp_act.atnaujinti_studiju_programa(studiju_programa, pavadinimas)
                flash("Sekmingai atnaujinta")
                return app.redirect(url_for('studiju_programos'))
            except Exception as e:
                zinute = e
                flash(e)
            return render_template("studiju_programos_forma_update.html", form=form, id=id)  
    
    @app.route('/studiju_programos_delete/<id>', methods=['GET', 'POST'])
    def st_pr_delete(id):
        sp_act.salinti_studiju_programa(id)
        flash("Sekmingai pasalinta")
        return app.redirect(url_for('studiju_programos'))
    