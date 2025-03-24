from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from models.studento_pasiekimai import StudentoPasiekimai
from forms.studento_pasiekimaiForma import StudentoPasiekimaiForma
from datetime import date  
from sqlalchemy import select

def init_studento_pasiekimas_routes(app):

    @app.route('/studento_pasiekimas', methods=['GET', 'POST'])
    @login_required
    def studento_pasiekimas():
        form = StudentoPasiekimaiForma()
        
        if form.validate_on_submit():
            studentas_id = form.studentas.data.id
            paskaita_id = form.paskaita.data.id 
            pazymys = form.pazymys.data
            nedalyvavo = form.nedalyvavo.data
            data = date.today()  

            pasiekimai = StudentoPasiekimai(
                studentas_id=studentas_id,
                paskaita_id=paskaita_id,
                pazymys=pazymys,
                nedalyvavo=nedalyvavo,
                data=data
            )
            
            db.session.add(pasiekimai)
            db.session.commit()
            flash("Studento pasiekimas išsaugotas sėkmingai!")
            return redirect(url_for('studento_pasiekimas'))

        return render_template('studento_pasiekimas_forma.html', form=form)

    @app.route('/studento_pasiekimas_perziura')
    @login_required
    def studento_pasiekimas_perziura():
        pasiekimas = db.session.execute(select(StudentoPasiekimai)).scalars().all()
        return render_template('studento_aktyvumas_perziura.html', pasiekimas=pasiekimas)