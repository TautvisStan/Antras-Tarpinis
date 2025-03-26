from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from sqlalchemy import select
from wtforms import DateField, StringField, SubmitField
from wtforms.validators import DataRequired\
    
# import from services. models, extensions
import services.tvarkarastis as tvarkarastis  
from models.kalendorius import Kalendorius
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
            tvarkarastis_data = tvarkarastis.gauti_vartotojo_tvarkarasti(current_user)  # Pakeistas importo pavadinimas
            return render_template('studento_tvarkarastis.html',
                                 studentas=current_user,
                                 paskaitos=tvarkarastis_data['paskaitos'],
                                 atsiskaitymai=tvarkarastis_data['atsiskaitymai'],
                                 egzaminai=tvarkarastis_data['egzaminai'],
                                 sventes=tvarkarastis_data['sventes'])
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('index'))

