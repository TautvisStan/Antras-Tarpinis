from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
import flask_login
from extensions import login_manager, Prisijunges
from services.dekoratoriai import turi_buti_atsijunges
from services.grupe_actions import automatiskai_priskirti_grupe
from services.mail_patvirtinimas import confirm_token, generate_token, send_email
import services.registracija_prisijungimas_actions as reg_pr
from forms.loginForma import LoginForma
from forms.registerForma import RegisterForma
import services.issaugoti_paveiksleli as iss_pav
import re


def init_login_routes(app):
    el_pasto_regex = r"^\S+@\S+\.\S+$" 
    pass_regex = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    
    @login_manager.unauthorized_handler
    def neprisijunges():
        return redirect(url_for("error_401"))
    
    @app.route('/403')
    @flask_login.login_required
    def error_403():
        return render_template('403.html')

    @app.route('/401')
    def error_401():
        return render_template('401.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    @turi_buti_atsijunges
    def login():
        form = LoginForma()
        if form.validate_on_submit():
            el_pastas = form.el_pastas.data
            if re.match(el_pasto_regex, el_pastas):
                
                slaptazodis = form.slaptazodis.data
                vartotojas = reg_pr.rasti_vartotoja(el_pastas, slaptazodis) 
                
                if vartotojas:

                    if reg_pr.patikrinti_blokavima(vartotojas):
                        flash("Jūsų paskyra blokuota, bandykite vėliau")
                        return redirect(url_for('login'))

                    if vartotojas and vartotojas.el_pat and vartotojas.dest_pat is not False:
                        prisijunges = Prisijunges(vartotojas.vaidmuo, vartotojas.studiju_programa_id)
                        prisijunges.id = vartotojas.id
                        flask_login.login_user(prisijunges)
                        flash("Sėkmingai prisijungta")
                        return redirect(url_for('protected'))   #TODO paskirstyti pagal roles (studentas.html, destytojas.html, admin.html)
            else:
                reg_pr.nesekmingu_prisijungimu_skaicius(vartotojas) 
                flash("Blogas prisijungimas!")
        
        return render_template("login_forma.html", form=form)
    
    @app.route('/register', methods=['GET', 'POST'])
    @turi_buti_atsijunges
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
                    vaidmuo = form.vaidmuo.data 
                    dest_pat = None
                    if vaidmuo == "Dėstytojas":             #destytojams bus reikalingas papildomas admin patvirtinimas
                        dest_pat = False
                    studiju_programa = form.studiju_programa.data.id
 

                    token = generate_token(el_pastas)
                    confirm_url = url_for("confirm_email", token=token, _external=True)
                    html = render_template("confirm_email.html", confirm_url=confirm_url)
                    subject = "Please confirm your email"
                    send_email(el_pastas, subject, html)


                                    # Jei įkeltas paveikslėlis, išsaugome jį
                    profilio_pav = None
                    ikelimo_data = None
                    print("TEST PROFILIO PAV")
                    if form.profilio_pav.data:
                        print("BUS PROFILIO PAV")
                        failo_pavadinimas = iss_pav.issaugoti_profilio_paveiksleli(form.profilio_pav.data, el_pastas)
                        if failo_pavadinimas:
                            profilio_pav = failo_pavadinimas
                            ikelimo_data = datetime.now()
                            flash('Profilio paveikslelis sekmingai ikeltas')
                        else:
                            flash('Netinkamas paveikslelio formatas arba dydis')


                    reg_pr.registruoti_vartotoja(vardas, pavarde, el_pastas, slaptazodis_hash, vaidmuo, studiju_programa, dest_pat, profilio_pav, ikelimo_data)
                    flash("Užregistruota!")

                    return redirect(url_for("index"))
                else:
                    flash("Blogas slaptažodis! Turi būti bent: 1 mažoji, 1 didžioji, 1 skaičius, 8 viso")
            else:

                flash("Blogas el. pašto adresas!")
        
        return render_template("register_forma.html", form=form)


    @app.route('/protected')    #TODO
    @flask_login.login_required
    def protected():
        return 'Logged in as: ' + str(flask_login.current_user.id) + " " + flask_login.current_user.vaidmuo


    @app.route('/logout')   
    @flask_login.login_required
    def logout():
        flask_login.logout_user()
        flash("Atsijungta!")
        return redirect(url_for('index'))
    

    @app.route("/confirm/<token>")
    def confirm_email(token):
        email = confirm_token(token)
        user = reg_pr.gauti_vartotoja_email(email)
        if user.el_pastas == email:
            reg_pr.patvirtinti_vartotojo_mail(user)
            if user.vaidmuo == "Studentas":
                automatiskai_priskirti_grupe(user)
            flash("You have confirmed your account. Thanks!", "success")
        else:
            flash("The confirmation link is invalid or has expired.", "danger")
        return redirect(url_for("index"))
