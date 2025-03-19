from flask import flash, redirect, render_template, request, url_for
import flask_login
from extensions import login_manager, Prisijunges
import services.registracija_prisijungimas_actions as reg_pr
from forms.loginForma import LoginForma
from forms.registerForma import RegisterForma
import re


def init_login_routes(app):
    el_pasto_regex = r"^\S+@\S+\.\S+$"  #TODO regex patikrinimas slaptazodziui

    @app.route('/401')
    @login_manager.unauthorized_handler
    def neprisijunges():
        return render_template('401.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForma()
        if form.validate_on_submit():
            el_pastas = form.el_pastas.data
            if re.match(el_pasto_regex, el_pastas):
                slaptazodis = form.slaptazodis.data
                vartotojas = reg_pr.rasti_vartotoja(el_pastas, slaptazodis) 
                if vartotojas:
                    prisijunges = Prisijunges(vartotojas.vaidmuo)
                    prisijunges.id = vartotojas.id
                    flask_login.login_user(prisijunges)
                    return redirect(url_for('protected'))   #TODO
            return 'Bad login'  #TODO
        
        return render_template("login_forma.html", form=form)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForma()
        if form.validate_on_submit():
            vardas = form.vardas.data
            pavarde = form.pavarde.data
            el_pastas = form.el_pastas.data
            
            if re.match(el_pasto_regex, el_pastas) and reg_pr.patikrinti_ar_nera(el_pastas):
                slaptazodis = form.slaptazodis.data
                slaptazodis_hash = reg_pr.gauti_slapt_hash(slaptazodis)
                vaidmuo = form.vaidmuo.data #TODO
                print(vaidmuo)
                reg_pr.registruoti_vartotoja(vardas, pavarde, el_pastas, slaptazodis_hash, vaidmuo)
                return "uzregistruotas"  #TODO
            
            flash("Neteisinga registracija!")
            return render_template("register_forma.html", form=form)
        
        return render_template("register_forma.html", form=form)


    @app.route('/protected')    #TODO
    @flask_login.login_required
    def protected():
        return 'Logged in as: ' + str(flask_login.current_user.id) + " " + str(flask_login.current_user.vaidmuo)


    @app.route('/logout')   #TODO
    @flask_login.login_required
    def logout():
        flask_login.logout_user()
        return 'Logged out'