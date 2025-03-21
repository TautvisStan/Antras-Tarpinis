
from flask import flash, render_template, request, url_for
import services.grupe_actions as gr_act
from forms.GrupesForma import GrupesForma
def init_grupes_routes(app):
    @app.route('/grupes')
    def grupes():
        try:
            grupes = gr_act.view_grupes()
            return render_template('grupes.html', grupes = grupes)
        except Exception as e:
            flash(str(e), "danger")
            return render_template('grupes.html', grupes=[])

    @app.route('/grupes_create', methods=['GET', 'POST'])
    def gr_create():
        form = GrupesForma()
        if request.method == 'GET':
            return render_template("grupes_forma.html", form=form)
        else:    
            try:
                pavadinimas = form.pavadinimas.data
                gr_act.sukurti_grupe(pavadinimas)
                flash("Sekmingai sukurta", "success")
                return app.redirect(url_for('grupes'), 302)
            except Exception as e:
                flash(str(e), "danger")
            return render_template("grupes_forma.html", form=form)  
    
    @app.route('/grupes_update/<id>', methods=['GET', 'POST'])
    def gr_update(id):
        try:
            grupe = gr_act.gauti_grupe(id)
            form = GrupesForma(obj=grupe)
            
            if request.method == 'GET':
                return render_template("grupes_forma_update.html", form=form, id=id)
            else:    
                pavadinimas = form.pavadinimas.data
                gr_act.atnaujinti_grupe(grupe, pavadinimas)
                flash("Sekmingai atnaujinta","success")
                return app.redirect(url_for('grupes'))
        except Exception as e:
            flash(str(e), "danger")
            return render_template("grupes_forma_update.html", form=form, id=id)  

    @app.route('/grupes_delete/<id>', methods=['GET', 'POST'])
    def gr_delete(id):
        try:
            gr_act.salinti_grupe(id)
            flash("Sekmingai pasalinta", "success")
            return app.redirect(url_for('grupes'))
        except Exception as e:
            flash(str(e), "danger")