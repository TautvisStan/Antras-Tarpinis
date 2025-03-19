from flask import flash, redirect, render_template, request, url_for
import flask_login
from extensions import login_manager, Prisijunges
import services.registracija_prisijungimas_actions as reg_pr
from forms.loginForma import LoginForma
from forms.registerForma import RegisterForma
import re


def init_login_routes(app):
    el_pasto_regex = r"^\S+@\S+\.\S+$"  #TODO regex patikrinimas slaptazodziui
    pass_regex = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    
    @login_manager.unauthorized_handler
    def neprisijunges():
        return redirect(url_for("error_401"))
    
    @app.route('/401')
    def error_401():
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
                
            flash("Blogas prisijungimas!")
        
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
                if re.match(pass_regex, slaptazodis):
                    slaptazodis_hash = reg_pr.gauti_slapt_hash(slaptazodis)
                    vaidmuo = form.vaidmuo.data #TODO
                    print(vaidmuo)
                    reg_pr.registruoti_vartotoja(vardas, pavarde, el_pastas, slaptazodis_hash, vaidmuo)
                    return "uzregistruotas"  #TODO
                
                flash("Blogas slaptažodis! Turi būti bent: 1 mažoji, 1 didžioji, 1 skaičius, 8 viso")
            
            flash("Blogas el. pašto adresas!")
        
        return render_template("register_forma.html", form=form)


    @app.route("/test")
    def test():
        if flask_login.current_user.is_authenticated:
            return str(flask_login.current_user.vaidmuo) 
        return "neprisijunges"

    @app.route('/protected')    #TODO
    @flask_login.login_required
    def protected():
        return 'Logged in as: ' + str(flask_login.current_user.id) + " " + str(flask_login.current_user.vaidmuo)


    @app.route('/logout')   #TODO
    @flask_login.login_required
    def logout():
        flask_login.logout_user()
        return 'Logged out'