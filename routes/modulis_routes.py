from flask import flash, render_template, request, url_for
import services.modulis_actions as mo_act
from forms.modulisForma import ModulisForma
def init_modulis_routes(app):
    @app.route('/moduliai')
    def moduliai():
        return render_template('moduliai.html', moduliai = mo_act.view_modulis())

    @app.route('/moduliai_create', methods=['GET', 'POST'])
    def create():
        form = ModulisForma()
        if request.method == 'GET':
            return render_template("moduliai_forma.html", form=form)
        else:    
            try:
                pavadinimas = form.pavadinimas.data
                aprasymas = form.aprasymas.data
                kreditai = form.kreditai.data
                semestro_informacija = form.semestro_informacija.data
                mo_act.sukurti_moduli(pavadinimas, aprasymas, kreditai, semestro_informacija)
                flash("Sekmingai sukurta")
                return app.redirect(url_for('moduliai'), 302)
            except Exception as e:
                zinute = e
            return render_template("moduliai_forma.html", form=form)  
    
    @app.route('/moduliai_edit/<id>', methods=['GET', 'POST'])
    def update(id):
        modulis = mo_act.gauti_moduli(id)
        form = ModulisForma(obj=modulis)
        if request.method == 'GET':
            return render_template("moduliai_forma_update.html", form=form, id=id)
        else:    
            try:
                pavadinimas = form.pavadinimas.data
                aprasymas = form.aprasymas.data
                kreditai = form.kreditai.data
                semestro_informacija = form.semestro_informacija.data
                mo_act.atnaujinti_moduli(modulis, pavadinimas, aprasymas, kreditai, semestro_informacija)
                flash("Sekmingai atnaujinta")
                return app.redirect(url_for('moduliai'))
            except Exception as e:
                zinute = e
                flash(e)
            return render_template("moduliai_forma_update.html", form=form, id=id)  
    
    @app.route('/moduliai_delete/<id>', methods=['GET', 'POST'])
    def delete(id):
        mo_act.salinti_moduli(id)
        flash("Sekmingai pasalinta")
        return app.redirect(url_for('moduliai'))
    