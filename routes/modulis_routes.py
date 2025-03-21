from flask import flash, render_template, request, url_for
from flask_login import current_user
from services.dekoratoriai import Roles_Patikrinimas
import services.modulis_actions as mo_act
from forms.modulisForma import ModulisForma

from services.registracija_prisijungimas_actions import patikrinti_roles

from extensions import db   #TODO
from sqlalchemy import select
from models.vartotojas import Vartotojas


def init_modulis_routes(app):

    @app.route('/moduliai')
    def moduliai():
        try:
            moduliai = mo_act.view_modulis()
            return render_template('moduliai.html', moduliai = moduliai)
        except Exception as e:
            flash(str(e), "danger")
            return render_template('moduliai.html', moduliai=[])
    
    @app.route('/moduliai_create', methods=['GET', 'POST'])
    @Roles_Patikrinimas(["Dėstytojas", "Admin", "Studentas"])
    def create():
        # if patikrinti_roles(["Dėstytojas", "Admin"]) is False:
        #     return app.redirect(url_for('error_403'))
        
        form = ModulisForma()
        if request.method == 'GET':
            return render_template("moduliai_forma.html", form=form)
        else:    
            try:
                pavadinimas = form.pavadinimas.data
                aprasymas = form.aprasymas.data
                kreditai = form.kreditai.data
                semestro_informacija = form.semestro_informacija.data

                destytojas_id = current_user.id
                studiju_programa = db.session.get(Vartotojas.id).studiju_programa_id

                mo_act.sukurti_moduli(pavadinimas, aprasymas, kreditai, semestro_informacija, destytojas_id, studiju_programa)
                flash("Sekmingai sukurta", "success")
                return app.redirect(url_for('moduliai'), 302)
            except Exception as e:
                flash(str(e), "danger")
            return render_template("moduliai_forma.html", form=form)  
     
    @app.route('/moduliai_edit/<id>', methods=['GET', 'POST'])
    def update(id):
        try:
            modulis = mo_act.gauti_moduli(id)
            form = ModulisForma(obj=modulis)
        except Exception as e:
            flash(str(e), "danger")
            return app.redirect(url_for('moduliai'))
        
        if request.method == 'GET':
            return render_template("moduliai_forma_update.html", form=form, id=id)
        else:    
            try:
                pavadinimas = form.pavadinimas.data
                aprasymas = form.aprasymas.data
                kreditai = form.kreditai.data
                semestro_informacija = form.semestro_informacija.data

                mo_act.atnaujinti_moduli(modulis, pavadinimas, aprasymas, kreditai, semestro_informacija)
                flash("Sekmingai atnaujinta", "success")
                return app.redirect(url_for('moduliai'))
            except Exception as e:
                flash(str(e), "danger")
            return render_template("moduliai_forma_update.html", form=form, id=id)  
    
    @app.route('/moduliai_delete/<id>', methods=['GET', 'POST'])
    def delete(id):
        try:
            mo_act.salinti_moduli(id)
            flash("Sekmingai pasalinta","success")
            return app.redirect(url_for('moduliai'))
        except Exception as e:
            flash(str(e), "danger")
        return app.redirect(url_for('moduliai'))
        
    @app.route('/moduliai_view/<id>', methods=['GET', 'POST'])
    def view(id):
        try:
            modulis = mo_act.gauti_moduli(id)
            return render_template('modulio_perziura.html',modulis=modulis)
        except Exception as e:
            flash(str(e), "danger")
            return app.redirect(url_for('moduliai'))


    