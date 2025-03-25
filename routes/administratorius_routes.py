from flask import render_template, flash,redirect, url_for
from extensions import db
import services.administratorius_actions as ad_act
from forms.vartotojasForma import VartotojasForma
from flask import request,flash,url_for,redirect
from services.administratorius_actions import gauti_statistika
from flask_login import login_required, current_user
from sqlalchemy import select
from models.vartotojas import Vartotojas
from services.administratorius_actions import istrinti_vartotoja, uzblokuoti_vartotoja
from werkzeug.security import generate_password_hash


def init_administratorius_routes(app):
    @app.route('/statistika')
    def atvaizduoti_statistika():
        try:
            vartotoju_skaicius,moduliu_skaicius,studiju_programu_skaicius,grupiu_skaicius = ad_act.gauti_statistika()
            
            return render_template('statistika.html', vartotoju_skaicius=vartotoju_skaicius,moduliu_skaicius=moduliu_skaicius,studiju_programu_skaicius=studiju_programu_skaicius,grupiu_skaicius=grupiu_skaicius)
        except Exception as e:
            flash(str(e),"danger")

    @app.route('/administratorius/vartotojai')
    def vartotojai():
        try:
            vartotojai = ad_act.gauti_vartotojus()
            return render_template ('administratorius_vartotojai.html', vartotojai = vartotojai)
        except Exception as e:
            flash(str(e), "danger")
            return render_template('administratorius_vartotojai.html', vartotojai=[])
        
    @app.route('/administratorius/vartotojai/perziureti/<id>', methods=['GET', 'POST'])
    def perziureti_vartotoja(id):
        try:
            vartotojas = ad_act.gauti_vartotoja(id)
            return render_template('vartotojo_perziura.html',vartotojas=vartotojas)
        except Exception as e:
            flash(str(e), "danger")
            return redirect(url_for('vartotojai'))
    
    @app.route('/administratorius/vartotojai/sukurti', methods=['GET', 'POST'])
    def sukurti_nauja_vartotoja():
        
        form = VartotojasForma()
        if request.method == 'GET':
            return render_template('vartotojas_forma.html', form=form)
        else:
            try:
                vardas = form.vardas.data
                pavarde = form.pavarde.data
                vaidmuo = form.vaidmuo.data
                studiju_programa_id = form.studiju_programa.data.id if form.studiju_programa.data else None
                fakultetas_id = form.fakultetas.data.id if form.fakultetas.data else None
                el_pastas = form.el_pastas.data
                password = form.password.data

                password_hash = generate_password_hash(password)

                ad_act.sukurti_vartotoja(vardas,pavarde,vaidmuo,studiju_programa_id,fakultetas_id,el_pastas,password_hash)
                flash("Vartotojas sukurtas sėkmingai.","success")
                return redirect(url_for('vartotojai'))
                # return redirect('/administratorius/vartotojai')
            except Exception as e:
                flash(str(e), "danger")
            return render_template("vartotojas_forma.html", form=form)  

    @app.route('/administratorius/vartotojai/redaguoti/<id>', methods=['GET', 'POST'])
    def redaguoti_vartotoja(id):
        try:
            vartotojas = ad_act.gauti_vartotoja(id)
            form = VartotojasForma(obj = vartotojas)
        except Exception as e:
            flash(str(e), "danger")
            return redirect(url_for('vartotojai'))

        if request.method == 'GET':
            return render_template('vartotojas_forma_redaguoti.html', form=form, id=id)
        else:
                try:
                    vardas = form.vardas.data
                    pavarde = form.pavarde.data
                    vaidmuo = form.vaidmuo.data
                    ad_act.redaguoti_vartotoja(vartotojas,vardas,pavarde,vaidmuo)
                    flash("Vartotojas sėkmingai atnaujintas", "success")
                    return redirect(url_for('vartotojai'))
                except Exception as e:
                    flash(str(e), "danger")

                return render_template('vartotojas_forma_redaguoti.html', form=form, id=id)   
       
    @app.route('/administratorius/vartotojai/istrinti/<id>', methods=['GET', 'POST'])
    def panaikinti_vartotoja(id):
        try:
            ad_act.pasalinti_vartotoja(id)
            flash("Vartotojas sėkmingai pašalintas","success")
        except Exception as e:
            flash(str(e), "danger")
        return redirect(url_for('vartotojai'))
    

    @app.route('/istrinti_vartotoja/<id>', methods = ['POST'])
    @login_required
    def istrinti_vartotoja(id):
        if current_user.vaidmuo != 'admin':
            flash("Jums ši teisė nesuteikta", "warning")
            return redirect(url_for('atvaizduoti_statistika'))
        
        try:
            vartotojas = db.session.execute(select(Vartotojas).filter_by(id=id)).scalar()
            if not vartotojas:
                flash('Vartotojas nerastas', "warning")
                return redirect(url_for('atvaizduoti_statistika'))
            
            istrinti_vartotoja(vartotojas)
            flash(f'Vartotojas {vartotojas.vardas} {vartotojas.pavarde} buvo pašalintas')
            return redirect(url_for('atvaizduoti_statistika'))
        except Exception as e:
            flash(str(e), "danger")
            return redirect(url_for('atvaizduoti_statistika'))
        
    
    @app.route('/uzblokuoti_vartotoja/<id>', methods = ['POST'])
    @login_required
    def uzblokuoti_vartotoja(id):
        
        try:
            vartotojas = db.session.execute(select(Vartotojas).filter_by(id=id)).scalar()
            if not vartotojas:
                flash('Vartotojas nerastas',"warning")
                return redirect(url_for('atvaizduoti_statistika'))
            
            uzblokuoti_vartotoja(vartotojas)
            flash(f'Vartotojas {vartotojas.vardas} {vartotojas.pavarde} buvo užblokuotas')
            return redirect(url_for('atvaizduoti_statistika'))
        except Exception as e:
            flash(str(e), "danger")
            return redirect(url_for('atvaizduoti_statistika'))
            
            
