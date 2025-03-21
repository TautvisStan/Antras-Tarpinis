from flask import render_template,flash,redirect,url_for
import services.studentas_actions as st_act

def init_student_routes(app):
    @app.route('/studentai')
    def studentai():
        try:
            vartotojai=st_act.perziureti_studentus()
            return render_template('studentas.html', vartotojai= vartotojai)
        except Exception as e:
            flash(str(e), "danger")
            return render_template('studentas.html', vartotojai=[])
    
    @app.route('/studentas_perziureti/<id>', methods=['GET', 'POST'])
    def perziureti_studenta(id):
        try:
            studentas = st_act.gauti_studenta(id)
            return render_template('studento_perziura.html',vartotojas = studentas)
        except Exception as e:
            flash(str(e), "danger")
            return redirect(url_for('studentai'))