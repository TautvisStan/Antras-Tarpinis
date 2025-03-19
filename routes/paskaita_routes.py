from flask import render_template, redirect, url_for, flash, request
from extensions import db
from models.paskaita import Paskaita
from forms.paskaitaForma import PaskaitaForma
import services.paskaita_actions as pas_act

def init_paskaita_routes(app):
    @app.route('/paskaitos')
    def paskaitos():
        return render_template('paskaitos.html', paskaitos = pas_act.view_paskaitos())

    @app.route('/paskaita_create', methods=['GET', 'POST'])
    def paskaita_create():
        form = PaskaitaForma()
        if request.method == 'GET':
            return render_template("paskaita_forma.html", form=form)
        else:
            try:
               pavadinimas = form.pavadinimas.data
               savaites_diena = form.savaites_diena.data
               laikas_nuo = form.laikas_nuo.data
               laikas_iki = form.laikas_iki.data
               modulis_id = form.modulis_id.data

               pas_act.sukurti_paskaita(pavadinimas, savaites_diena, laikas_nuo, laikas_iki, modulis_id)
               flash("Sekmingai sukurta")
               return redirect(url_for('paskaitos'))
            except Exception as e:
                zinute = e
                flash(e)
            return render_template('paskaita_forma.html', form=form)

    @app.route('/paskaita_view/<id>', methods=['GET', 'POST'])
    def paskaita_view(id):
        paskaita = pas_act.gauti_paskaita(id)
        return render_template('paskaita_perziura.html', paskaita = paskaita)
    
    @app.route('/paskaita_delete/<id>', methods=['GET', 'POST'])
    def paskaita_delete(id):
        pas_act.salinti_paskaita(id)
        flash("Sekmingai pasalinta")
        return app.redirect(url_for('paskaitos'))

    @app.route('paskaita_edit/<id>', methods=['GET', 'POST'])
    def paskaita_update(id):
        paskaita = pas_act.gauti_paskaita(id)
        form = PaskaitaForma(obj = paskaita)
        if request.method == 'GET':
            return render_template('paskaita_forma_update.html', form = form, id = id)
        else:
            try:
                pavadinimas = form.pavadinimas.data
                savaites_diena = form.savaites_diena.data
                laikas_nuo = form.laikas_nuo.data
                laikas_iki = form.laikas_iki.data
                modulis_id = form.modulis_id.data
                pas_act.atnaujinti_paskaita(paskaita, savaites_diena, laikas_nuo, laikas_iki, modulis_id)
                flash("Sekmingai atnaujinta")
                return app.redirect(url_for('paskaitos'))
            except Exception as e:
                zinute = e
                flash(e)
            return render_template("paskaita_forma_update.html", form=form, id=id)  
    

    
  