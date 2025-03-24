from flask import flash, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from extensions import db
from sqlalchemy import select
from forms.testasForma import TestasForma  # Reikės sukurti šią formą
from models.studentai_moduliai import StudentasModulis
from models.testas import Testas
import services.testas_actions as testas_act

def init_testas(app):
    @app.route('/testai/naujas/<int:modulis_id>', methods=['GET', 'POST'])
    @login_required
    def testai_create(modulis_id):
        if current_user.vaidmuo != 'destytojas':
            flash('Tik dėstytojai gali kurti testus', 'error')
            return redirect(url_for('moduliai'))
        
        form = TestasForma()
        if form.validate_on_submit():
            try:
                klausimai_data = [
                    {'tekstas': klausimas.tekstas.data, 'atsakymas': klausimas.atsakymas.data}
                    for klausimas in form.klausimai
                ]
                testas_act.sukurti_testa(
                    pavadinimas=form.pavadinimas.data,
                    modulis_id=modulis_id,
                    atsiskaitymas_id=form.atsiskaitymas.data.id if form.atsiskaitymas.data else None,
                    klausimai_data=klausimai_data,
                    maksimalus_balas=form.maksimalus_balas.data
                )
                flash("Testas sėkmingai sukurtas", "success")
                return redirect(url_for('moduliai'))
            except Exception as e:
                flash(f"Klaida kuriant testą: {str(e)}", "error")
        return render_template("testai_forma.html", form=form, modulis_id=modulis_id)

    @app.route('/testai/sprendimas/<int:testo_id>', methods=['GET', 'POST'])
    @login_required
    def testai_solve(testo_id):
        if current_user.vaidmuo != 'studentas':
            flash('Tik studentai gali spręsti testus', 'error')
            return redirect(url_for('index'))
        
        testas = testas_act.gauti_testa(testo_id)
        if request.method == 'POST':
            try:
                atsakymai = request.form.to_dict()
                rezultatas = testas_act.pateikti_testo_atsakymus(testo_id, atsakymai)
                flash(f"Jūsų rezultatas: {rezultatas.rezultatas}/{testas.maksimalus_balas}", "success")
                return redirect(url_for('index'))
            except Exception as e:
                flash(f"Klaida sprendžiant testą: {str(e)}", "error")
        return render_template("testai_sprendimas.html", testas=testas)
    
    @app.route('/mano_pazymiai')
    @login_required
    def mano_pazymiai():
        if current_user.vaidmuo != 'studentas':
            flash('Tik studentai gali matyti savo pažymius', 'error')
            return redirect(url_for('index'))
        
        pazymiai = db.session.execute(
            select(StudentasModulis).where(StudentasModulis.studentas_id == current_user.id)
        ).scalars().all()
        return render_template('mano_pazymiai.html', pazymiai=pazymiai)