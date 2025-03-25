# from flask import render_template, redirect, url_for, flash, request
# from extensions import db
# from models.atsiskaitymas import Atsiskaitymas
# from flask import render_template,redirect, url_for, flash
# from flask_login import login_required
# from forms.atsiskaitymasForma import AtsiskaitymasForma
# import services.atsiskaitymas_actions as ats_act

# def init_atsiskaitymas_routes(app):
#     @app.route('/atsiskaitymai')
#     def atsiskaitymai():
#         try:
#             atsiskaitymai=ats_act.view_atsiskaitymai()
#             return render_template('atsiskaitymai.html', atsiskaitymai=atsiskaitymai)
#         except Exception as e:
#             flash(str(e), "danger")
#             return render_template('atsiskaitymai.html', atsiskaitymai=[])

#     @app.route('/atsiskaitymas_create', methods=['GET', 'POST'])
#     def atsiskaitymas_create():
#         form = AtsiskaitymasForma()
#         if request.method == 'POST' and form.validate_on_submit():
#             try:
#                 pavadinimas = form.pavadinimas.data
#                 data_nuo = form.data_nuo.data
#                 data_iki = form.data_iki.data
#                 aprasymas = form.aprasymas.data
#                 modulis_id = form.modulis.data.id if form.modulis.data else None

#                 ats_act.sukurti_atsiskaityma(pavadinimas, data_nuo, data_iki, aprasymas, modulis_id)
#                 flash("Sekmingai sukurta", "success")
#                 return redirect(url_for('atsiskaitymai'))
#             except Exception as e:
#                 flash(str(e), "danger")
#         return render_template('atsiskaitymas_forma.html', form=form)

#     @app.route('/atsiskaitymas_view/<id>')
#     def atsiskaitymas_view(id):
#         try:
#             atsiskaitymas = ats_act.gauti_atsiskaityma(id)
#             return render_template('atsiskaitymas_perziura.html', atsiskaitymas=atsiskaitymas)
#         except Exception as e:
#             flash(str(e), "danger")
#             return redirect(url_for('atsiskaitymai'))           

#     @app.route('/atsiskaitymas_delete/<id>', methods=['POST'])
#     def atsiskaitymas_delete(id):
#         try:
#             ats_act.salinti_atsiskaityma(id)
#             flash("Sekmingai pasalinta", "success")
#         except Exception as e:
#             flash(str(e), "danger")
#         return redirect(url_for('atsiskaitymai'))

#     @app.route('/atsiskaitymas_edit/<id>', methods=['GET', 'POST'])
#     def atsiskaitymas_update(id):
#         try:
#             atsiskaitymas = ats_act.gauti_atsiskaityma(id)
#         except Exception as e:
#                 flash(str(e), "danger")
#                 return redirect(url_for('atsiskaitymai'))

#         form = AtsiskaitymasForma(obj=atsiskaitymas)
#         if request.method == 'POST' and form.validate_on_submit():
#             try:
#                 pavadinimas = form.pavadinimas.data
#                 data_nuo = form.data_nuo.data
#                 data_iki = form.data_iki.data
#                 aprasymas = form.aprasymas.data
#                 modulis_id = form.modulis.data.id if form.modulis.data else None

#                 ats_act.atnaujinti_atsiskaityma(atsiskaitymas, pavadinimas, data_nuo, data_iki, aprasymas, modulis_id)
#                 flash("Sekmingai atnaujinta", "success")
#                 return redirect(url_for('atsiskaitymai'))
#             except Exception as e:
#                 flash(str(e), "danger")
#         return render_template("atsiskaitymas_forma_update.html", form=form, id=id)
    
#     def create_atsiskaitymas():
#         form = AtsiskaitymasForma()
#         if form.validate_on_submit():
#             try:
#                 data = form.data.data
#                 aprasymas = form.aprasymas.data
#                 modulis_id = form.modulis.data.id  
#                 atsiskaitymas = ats_act.priskirti_atsiskaityma_moduliui(data, aprasymas, modulis_id)
#                 flash("Atsiskaitymas sėkmingai sukurtas!","success")
#                 return redirect(url_for('atsiskaitymai'))  
#             except Exception as e:
#                 flash(str(e), "danger")
#         return render_template('atsiskaitymas_forma.html', form=form)
