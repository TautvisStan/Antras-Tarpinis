from flask import render_template, redirect, url_for, flash, request
from extensions import db
from models.paskaita import Paskaita
from forms.paskaitaForma import PaskaitaForma
import services.paskaita_actions as pas_act

def init_paskaita_routes(app):
    @app.route('/paskaitos')
    def paskaitos():
        try:
            return render_template('paskaitos.html', paskaitos=pas_act.view_paskaitos())
        except Exception as e:
            flash(str(e), "danger")

    @app.route('/paskaita_create', methods=['GET', 'POST'])
    def paskaita_create():
        form = PaskaitaForma()
        if request.method == 'POST' and form.validate_on_submit():
            try:
                pavadinimas = form.pavadinimas.data
                savaites_diena = form.savaites_diena.data
                laikas_nuo = form.laikas_nuo.data
                laikas_iki = form.laikas_iki.data
                modulis_id = form.modulis_id.data.id if form.modulis_id.data else None

                pas_act.sukurti_paskaita(pavadinimas, savaites_diena, laikas_nuo, laikas_iki, modulis_id)
                flash("Sekmingai sukurta", "success")
                return redirect(url_for('paskaitos'))
            except Exception as e:
                flash(str(e), "danger")
        return render_template('paskaita_forma.html', form=form)

    @app.route('/paskaita_view/<id>')
    def paskaita_view(id):
        try:
            paskaita = pas_act.gauti_paskaita(id)
            if paskaita is None:
                flash("Paskaita nerasta", "danger")
                return redirect(url_for('paskaitos'))
            return render_template('paskaita_perziura.html', paskaita=paskaita)
        except Exception as e:
            flash(str(e), "danger")
            return redirect(url_for('paskaitos'))
    

    @app.route('/paskaita_delete/<id>', methods=['POST'])
    def paskaita_delete(id):
        try:
            pas_act.salinti_paskaita(id)
            flash("Sekmingai pasalinta", "success")
        except Exception as e:
            flash(str(e), "danger")
        return redirect(url_for('paskaitos'))

    @app.route('/paskaita_edit/<id>', methods=['GET', 'POST'])
    def paskaita_update(id):
        try:
            paskaita = pas_act.gauti_paskaita(id)
            if paskaita is None:
                flash("Paskaita nerasta", "danger")
                return redirect(url_for('paskaitos'))
        except Exception as e:
            flash(str(e), "danger")
            return redirect(url_for('paskaitos'))

        form = PaskaitaForma(obj=paskaita)
        if request.method == 'POST' and form.validate_on_submit():
            try:
                pavadinimas = form.pavadinimas.data
                savaites_diena = form.savaites_diena.data
                laikas_nuo = form.laikas_nuo.data
                laikas_iki = form.laikas_iki.data
                modulis_id = form.modulis_id.data.id if form.modulis_id.data else None

                pas_act.atnaujinti_paskaita(paskaita, pavadinimas, savaites_diena, laikas_nuo, laikas_iki, modulis_id)
                flash("Sekmingai atnaujinta", "success")
                return redirect(url_for('paskaitos'))
            except Exception as e:
                flash(str(e), "danger")
        return render_template("paskaita_forma_update.html", form=form, id=id)