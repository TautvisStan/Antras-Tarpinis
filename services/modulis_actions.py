from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from sqlalchemy import select
from wtforms import DateField, StringField, SubmitField
from wtforms.validators import DataRequired\
    
# import from services. models, extensions
import services.tvarkarastis as tvarkarastis  
from models.kalendorius import Kalendorius
from models.atsiskaitymas import Atsiskaitymas
from extensions import db

class KalendoriusForma(FlaskForm):
    data = DateField('Data', validators=[DataRequired()], format='%Y-%m-%d')
    aprasas = StringField('Aprašas')
    submit = SubmitField('Pridėti')

def init_vartotojas_routes(app):
    @app.route('/tvarkarastis')
    @login_required
    def studento_tvarkarastis():
        try:
            tvarkarastis_data = tvarkarastis.gauti_vartotojo_tvarkarasti(current_user)
            # Pridedame atsiskaitymus iš visų modulių
            atsiskaitymai = db.session.execute(select(Atsiskaitymas)).scalars().all()
            tvarkarastis_data['atsiskaitymai'] = sorted(atsiskaitymai, key=lambda x: x.data)
            return render_template('studento_tvarkarastis.html',
                                 studentas=current_user,
                                 paskaitos=tvarkarastis_data['paskaitos'],
                                 atsiskaitymai=tvarkarastis_data['atsiskaitymai'],
                                 egzaminai=tvarkarastis_data['egzaminai'],
                                 sventes=tvarkarastis_data['sventes'])
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('index'))

    @app.route('/kalendorius', methods=['GET', 'POST'])
    @login_required
    def kalendorius():
        if current_user.vaidmuo != 'admin':
            flash('Tik administratoriai gali valdyti kalendorių', 'error')
            return redirect(url_for('studento_tvarkarastis'))
        
        form = KalendoriusForma()
        if form.validate_on_submit():
            try:
                kalendorius = Kalendorius(
                    data=form.data.data,
                    aprasas=form.aprasas.data
                )
                db.session.add(kalendorius)
                db.session.commit()
                flash('Šventė sėkmingai pridėta!', 'success')
                return redirect(url_for('kalendorius'))
            except Exception as e:
                db.session.rollback()
                flash(f'Klaida pridedant šventę: {str(e)}', 'error')
        
        sventes = db.session.execute(select(Kalendorius)).scalars().all()
        return render_template('kalendorius.html', form=form, sventes=sventes)