from flask import render_template, flash,redirect, url_for
from extensions import db
from services.administratorius_actions import gauti_statistika
from flask_login import login_required, current_user
from sqlalchemy import select
from models.vartotojas import Vartotojas
from services.administratorius_actions import istrinti_vartotoja, uzblokuoti_vartotoja


def init_administratorius_routes(app):
    @app.route('/statistika')
    def atvaizduoti_statistika():
        vartotoju_skaicius,moduliu_skaicius,studiju_programu_skaicius,grupiu_skaicius = gauti_statistika()
        
        return render_template('statistika.html', vartotoju_skaicius = vartotoju_skaicius, moduliu_skaicius = moduliu_skaicius, studiju_programu_skaicius = studiju_programu_skaicius,grupiu_skaicius = grupiu_skaicius)


    @app.route('/istrinti_vartotoja/<id>', methods = ['POST'])
    @login_required
    def istrinti_vartotoja(id):
        if current_user.vaidmuo != 'admin':
            flash("Jums ši teisė nesuteikta")
            return redirect(url_for('atvaizduoti_statistika'))
        
        try:
            vartotojas = db.session.execute(select(Vartotojas).filter_by(id=id)).scalar()
            if not vartotojas:
                flash('Vartotojas nerastas')
                return redirect(url_for('atvaizduoti_statistika'))
            
            istrinti_vartotoja(vartotojas)
            flash(f'Vartotojas {vartotojas.vardas} {vartotojas.pavarde} buvo pašalintas')
            return redirect(url_for('atvaizduoti_statistika'))
        except Exception as e:
            flash(e)
            return redirect(url_for('atvaizduoti_statistika'))
        
    
    @app.route('/uzblokuoti_vartotoja/<id>', methods = ['POST'])
    @login_required
    def uzblokuoti_vartotoja(id):
        
        try:
            vartotojas = db.session.execute(select(Vartotojas).filter_by(id=id)).scalar()
            if not vartotojas:
                flash('Vartotojas nerastas')
                return redirect(url_for('atvaizduoti_statistika'))
            
            uzblokuoti_vartotoja(vartotojas)
            flash(f'Vartotojas {vartotojas.vardas} {vartotojas.pavarde} buvo užblokuotas')
            return redirect(url_for('atvaizduoti_statistika'))
        except Exception as e:
            flash(e)
            return redirect(url_for('atvaizduoti_statistika'))
            
            
