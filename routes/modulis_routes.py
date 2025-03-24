from flask import flash, render_template, url_for, redirect, request
from flask_login import current_user, login_required
from extensions import db
from sqlalchemy import select

from models.modulis import Modulis
from models.paskaita import Paskaita
from forms.modulisForma import ModulisForma
from forms.paskaitaForma import PaskaitaForma
import services.modulis_actions as mo_act

def init_modulis_routes(app):
    @app.route('/moduliai')
    @login_required
    def moduliai():
        if current_user.vaidmuo != 'destytojas':
            flash('Tik dėstytojai gali valdyti modulius', 'error')
            return redirect(url_for('index'))
        
        destytojo_moduliai = db.session.execute(select(Modulis).where(Modulis.destytojas_id == current_user.id)).scalars().all()
        return render_template('modulis_list.html', moduliai=destytojo_moduliai)
    
    @app.route('/moduliai_create', methods=['GET', 'POST'])
    @login_required
    def create():
        if current_user.vaidmuo != 'destytojas':
            flash('Tik dėstytojai gali kurti modulius', 'error')
            return redirect(url_for('index'))
        
        form = ModulisForma()
        if form.validate_on_submit():
            try:
                paskaita_data_list = [
                    {
                        'pavadinimas': paskaita.pavadinimas.data,
                        'savaites_diena': paskaita.savaites_diena.data,
                        'laikas_nuo': paskaita.laikas_nuo.data,
                        'laikas_iki': paskaita.laikas_iki.data
                    } for paskaita in form.paskaitos
                ]
                mo_act.sukurti_moduli(
                    pavadinimas=form.pavadinimas.data,
                    aprasymas=form.aprasymas.data,
                    kreditai=form.kreditai.data,
                    semestro_informacija=form.semestro_informacija.data,
                    destytojas_id=current_user.id,
                    studiju_programa_id=form.studiju_programa.data.id,
                    egzaminas_data=form.egzaminas_data.data,
                    paskaita_data_list=paskaita_data_list
                )
                flash("Sėkmingai sukurta", "success")
                return redirect(url_for('moduliai'))
            except Exception as e:
                flash(f"Klaida kuriant modulį: {str(e)}", "error")
        return render_template("moduliai_forma.html", form=form)
     
    @app.route('/moduliai_edit/<int:id>', methods=['GET', 'POST'])
    @login_required
    def update(id):
        if current_user.vaidmuo != 'destytojas':
            flash('Tik dėstytojai gali redaguoti modulius', 'error')
            return redirect(url_for('index'))
        
        modulis = mo_act.gauti_moduli(id)
        if not modulis or modulis.destytojas_id != current_user.id:
            flash('Modulis nerastas arba neturite teisių jį redaguoti', 'error')
            return redirect(url_for('moduliai'))
        
        form = ModulisForma(obj=modulis)
        if request.method == 'GET':
            form.paskaitos.entries.clear()
            for paskaita in modulis.paskaitos:
                paskaita_form = PaskaitaForma()
                paskaita_form.pavadinimas.data = paskaita.pavadinimas
                paskaita_form.savaites_diena.data = paskaita.savaites_diena
                paskaita_form.laikas_nuo.data = paskaita.laikas_nuo
                paskaita_form.laikas_iki.data = paskaita.laikas_iki
                form.paskaitos.append_entry(paskaita_form)

        if form.validate_on_submit():
            try:
                paskaita_data_list = [
                    {
                        'pavadinimas': paskaita.pavadinimas.data,
                        'savaites_diena': paskaita.savaites_diena.data,
                        'laikas_nuo': paskaita.laikas_nuo.data,
                        'laikas_iki': paskaita.laikas_iki.data
                    } for paskaita in form.paskaitos
                ]
                mo_act.atnaujinti_moduli(
                    modulis=modulis,
                    pavadinimas=form.pavadinimas.data,
                    aprasymas=form.aprasymas.data,
                    kreditai=form.kreditai.data,
                    semestro_informacija=form.semestro_informacija.data,
                    egzaminas_data=form.egzaminas_data.data,
                    paskaita_data_list=paskaita_data_list
                )
                flash("Sėkmingai atnaujinta", "success")
                return redirect(url_for('moduliai'))
            except Exception as e:
                flash(f"Klaida redaguojant modulį: {str(e)}", "error")
        return render_template("moduliai_forma_update.html", form=form, id=id)
    
    @app.route('/moduliai_delete/<int:id>', methods=['GET', 'POST'])
    @login_required
    def delete(id):
        if current_user.vaidmuo != 'destytojas':
            flash('Tik dėstytojai gali šalinti modulius', 'error')
            return redirect(url_for('index'))
        
        modulis = mo_act.gauti_moduli(id)
        if modulis and modulis.destytojas_id == current_user.id:
            try:
                mo_act.salinti_moduli(id)
                flash("Sėkmingai pašalinta", "success")
            except Exception as e:
                flash(f"Klaida šalinant modulį: {str(e)}", "error")
        else:
            flash("Modulis nerastas arba neturite teisių jį pašalinti", "error")
        return redirect(url_for('moduliai'))
    
    @app.route('/moduliai_view/<int:id>', methods=['GET', 'POST'])
    @login_required
    def view(id):
        if current_user.vaidmuo != 'destytojas':
            flash('Tik dėstytojai gali peržiūrėti modulius', 'error')
            return redirect(url_for('index'))
        
        modulis = mo_act.gauti_moduli(id)
        if not modulis or modulis.destytojas_id != current_user.id:
            flash("Modulis nerastas arba neturite teisių jį peržiūrėti", "error")
            return redirect(url_for('moduliai'))
        return render_template('modulio_perziura.html', modulis=modulis)
    