from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from forms.moduliu_pasirinkimasForma import ModuliuPasirinkimoForma
import services.studentas_modulis_actions as sm_act  

def init_studento_moduliu_routes(app):
    @app.route('/moduliai_pasirinkti', methods=['GET', 'POST'])
    @login_required
    def pasirinkti_modulius():
        form = ModuliuPasirinkimoForma()

        if form.validate_on_submit():
            try:
                
                pasirinkti_moduliai = form.moduliai.data
                if pasirinkti_moduliai:
                    
                    sm_act.sukurti_studento_modulius(current_user.id, pasirinkti_moduliai)
                    flash("Moduliai sėkmingai pasirinkti")
                    return redirect(url_for('index'))  
                else:
                    flash("Pasirinkite bent vieną modulį")
            except Exception as e:
                zinute = e
                flash(e)

        return render_template('moduliu_pasirinkimas.html', form=form)