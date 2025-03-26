from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import select
from forms.moduliu_pasirinkimasForma import ModuliuPasirinkimoForma
from models.modulis import Modulis
import services.studentas_modulis_actions as sm_act  
import services.atsiskaitymas_actions as ats_act
from extensions import db

def init_studento_moduliu_routes(app):
    @app.route('/moduliai_pasirinkti')
    @login_required
    def moduliai_pasirinkti():
        if current_user.vaidmuo != 'Studentas':
            flash('Tik studentai gali pasirinkti', 'error')
            return redirect(url_for('index'))
        
        pasirinkti_moduliai = db.session.execute(select(Modulis).where(Modulis.studiju_programa_id == current_user.studiju_programa_id)).scalars().all()
        return render_template('moduliu_pasirinkimas.html', moduliai=pasirinkti_moduliai)
    
    @app.route('/moduliai_pasirinkti/<id>')
    @login_required 
    def moduliai_pasirinkti_id(id):
        sm_act.sukurti_studento_modulius(current_user.id, id)
        flash("Modulias sėkmingai pasirinktas","success")
        return redirect(url_for('moduliai_pasirinkti'))  
#     @app.route('/moduliai_pasirinkti', methods=['GET', 'POST'])
#     @login_required
#     def pasirinkti_modulius():
#         form = ModuliuPasirinkimoForma()

#         if form.validate_on_submit():
#             try: 
#                 pasirinkti_moduliai = form.moduliai.data
#                 if pasirinkti_moduliai:
#                     sm_act.sukurti_studento_modulius(current_user.id, pasirinkti_moduliai)
#                     flash("Moduliai sėkmingai pasirinkti","success")
#                     return redirect(url_for('index'))  
#                 else:
#                     flash("Pasirinkite bent vieną modulį","warning")
#             except Exception as e:
#                flash(str(e), "danger")
#         return render_template('moduliu_pasirinkimas.html', form=form)
    

#     @app.route('/atsiskaitymai', methods=['GET'])
#     @login_required
#     def atsiskaitymai():
#         try:
#             studento_moduliai = sm_act.gauti_studento_modulius(current_user.id)
#             atsiskaitymai = []

#             for modulis in studento_moduliai:
#                 atsiskaitymai += ats_act.gauti_atsiskaitymus(modulis.modulis_id)
#             if not atsiskaitymai:
#                 flash("Nėra atsiskaitymų jūsų pasirinktų modulių.", "info")
                
#             return render_template('atsiskaitymai.html', atsiskaitymai=atsiskaitymai)
        
#         except Exception as e:
#             flash(str(e), "danger")

