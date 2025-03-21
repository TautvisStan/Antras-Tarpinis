from flask import render_template,redirect, url_for, flash
from flask_login import login_required
from forms.atsiskaitymasForma import AtsiskaitymasForma
import services.atsiskaitymas_actions as ats_act

def init_atsiskaitymas_routes(app):
    @app.route('/atsiskaitymas')
    def atsiskaitymas():
        return render_template('grupes.html', atsiskaitymas = ats_act.view_atsiskaitymai())

    @app.route('/atsiskaitymas_create', methods=['GET', 'POST'])
    def create_atsiskaitymas():
        form = AtsiskaitymasForma()
        if form.validate_on_submit():
            try:
            
                data = form.data.data
                aprasymas = form.aprasymas.data
                modulis_id = form.modulis.data.id  

            
                atsiskaitymas = ats_act.priskirti_atsiskaityma_moduliui(data, aprasymas, modulis_id)
                flash("Atsiskaitymas sėkmingai sukurtas!")
                return redirect(url_for('atsiskaitymai'))  
            except Exception as e:
                flash(e)

        return render_template('atsiskaitymas_forma.html', form=form)