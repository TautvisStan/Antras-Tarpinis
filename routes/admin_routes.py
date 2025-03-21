from flask import flash, redirect, render_template, request, url_for
import flask_login
from functools import wraps
from extensions import db
from models.vartotojas import Vartotojas
from models.modulis import Modulis
from models.grupes import Grupe
from models.studiju_programa import StudijuPrograma
import services.administratorius_actions as admin_actions
from forms.vartotojasForma import VartotojasForma
from services.registracija_prisijungimas_actions import gauti_slapt_hash
import services.issaugoti_paveiksleli as iss_pav
from datetime import datetime

# Administratoriaus teisių tikrinimo dekoratorius
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not flask_login.current_user.is_authenticated or flask_login.current_user.vaidmuo != "Administratorius":
            flash("Jūs neturite teisių pasiekti šį puslapį.", "danger")
            return redirect(url_for('error_403'))
        return f(*args, **kwargs)
    return decorated_function

def init_admin_routes(app):
    
    @app.route('/admin/vartotojai')
    @flask_login.login_required
    @admin_required
    def admin_vartotojai():
        vartotojai = admin_actions.gauti_vartotojus()
        paieska = request.args.get('paieska', '')
        
        if paieska:
            # Filtruojame vartotojus pagal paiešką
            vartotojai = [v for v in vartotojai if paieska.lower() in v.vardas.lower() or 
                          paieska.lower() in v.pavarde.lower() or 
                          paieska.lower() in v.el_pastas.lower()]
        
        return render_template('admin_vartotojai.html', vartotojai=vartotojai)
    
    @app.route('/admin/vartotojai/naujas', methods=['GET', 'POST'])
    @flask_login.login_required
    @admin_required
    def admin_naujas_vartotojas():
        form = VartotojasForma()
        
        if form.validate_on_submit():
            vardas = form.vardas.data
            pavarde = form.pavarde.data
            vaidmuo = form.vaidmuo.data
            el_pastas = form.el_pastas.data
            slaptazodis = form.slaptazodis.data
            studiju_programa = form.studiju_programa.data.id
            
            # Dėstytojams reikia patvirtinimo
            dest_pat = None
            if vaidmuo == "Dėstytojas":
                dest_pat = False
                
            # Slaptažodžio hash gavimas
            slaptazodis_hash = gauti_slapt_hash(slaptazodis)
            
            # Profilio paveikslėlio tvarkymas
            profilio_pav = None
            ikelimo_data = None
            if form.profilio_pav.data:
                failo_pavadinimas = iss_pav.issaugoti_profilio_paveiksleli(form.profilio_pav.data, el_pastas)
                if failo_pavadinimas:
                    profilio_pav = failo_pavadinimas
                    ikelimo_data = datetime.now()
                    flash('Profilio paveikslelis sekmingai ikeltas', 'success')
                else:
                    flash('Netinkamas paveikslelio formatas arba dydis', 'warning')
            
            # Naujo vartotojo sukūrimas
            try:
                admin_actions.sukurti_vartotoja(vardas, pavarde, vaidmuo, el_pastas, slaptazodis_hash, 
                                                studiju_programa, dest_pat, profilio_pav, ikelimo_data)
                flash(f"Vartotojas {vardas} {pavarde} sėkmingai sukurtas", "success")
                return redirect(url_for('admin_vartotojai'))
            except Exception as e:
                flash(f"Klaida kuriant vartotoją: {str(e)}", "danger")
        
        return render_template('admin_naujas_vartotojas.html', form=form)
    
    @app.route('/admin/vartotojai/redaguoti/<int:id>', methods=['GET', 'POST'])
    @flask_login.login_required
    @admin_required
    def admin_redaguoti_vartotoja(id):
        vartotojas = admin_actions.gauti_vartotoja(id)
        
        if not vartotojas:
            flash("Vartotojas nerastas", "danger")
            return redirect(url_for('admin_vartotojai'))
        
        form = VartotojasForma(obj=vartotojas)
        
        # Išjungiame slaptažodžio validaciją redagavimo atveju
        form.slaptazodis.validators = []
        form.slaptazodis.render_kw = {'disabled': 'disabled'}
        
        if form.validate_on_submit():
            vardas = form.vardas.data
            pavarde = form.pavarde.data
            vaidmuo = form.vaidmuo.data
            studiju_programa = form.studiju_programa.data.id
            
            # Update vartotojo duomenų
            try:
                admin_actions.redaguoti_vartotoja(vartotojas, vardas, pavarde, vaidmuo, studiju_programa)
                flash(f"Vartotojas {vardas} {pavarde} sėkmingai atnaujintas", "success")
                return redirect(url_for('admin_vartotojai'))
            except Exception as e:
                flash(f"Klaida atnaujinant vartotoją: {str(e)}", "danger")
        
        return render_template('admin_redaguoti_vartotoja.html', form=form, vartotojas=vartotojas)
    
    @app.route('/admin/vartotojai/istrinti/<int:id>', methods=['POST'])
    @flask_login.login_required
    @admin_required
    def admin_istrinti_vartotoja(id):
        try:
            admin_actions.istrinti_vartotoja(id)
            flash("Vartotojas sėkmingai ištrintas", "success")
        except Exception as e:
            flash(f"Klaida trinant vartotoją: {str(e)}", "danger")
        
        return redirect(url_for('admin_vartotojai'))
    
    @app.route('/admin/vartotojai/uzblokuoti/<int:id>')
    @flask_login.login_required
    @admin_required
    def admin_uzblokuoti_vartotoja(id):
        vartotojas = admin_actions.gauti_vartotoja(id)
        
        if not vartotojas:
            flash("Vartotojas nerastas", "danger")
            return redirect(url_for('admin_vartotojai'))
        
        try:
            admin_actions.uzblokuoti_vartotoja(vartotojas)
            flash(f"Vartotojas {vartotojas.vardas} {vartotojas.pavarde} sėkmingai užblokuotas", "success")
        except Exception as e:
            flash(f"Klaida blokuojant vartotoją: {str(e)}", "danger")
        
        return redirect(url_for('admin_vartotojai'))
    
    @app.route('/admin/vartotojai/atblokuoti/<int:id>')
    @flask_login.login_required
    @admin_required
    def admin_atblokuoti_vartotoja(id):
        vartotojas = admin_actions.gauti_vartotoja(id)
        
        if not vartotojas:
            flash("Vartotojas nerastas", "danger")
            return redirect(url_for('admin_vartotojai'))
        
        try:
            vartotojas.aktyvumas = True
            db.session.commit()
            flash(f"Vartotojas {vartotojas.vardas} {vartotojas.pavarde} sėkmingai atblokuotas", "success")
        except Exception as e:
            flash(f"Klaida atblokuojant vartotoją: {str(e)}", "danger")
        
        return redirect(url_for('admin_vartotojai'))
    
    @app.route('/admin/destytojai/patvirtinti')
    @flask_login.login_required
    @admin_required
    def admin_destytoju_patvirtinimas():
        # Gauti visus nepatvirtintus dėstytojus
        destytojai = db.session.execute(
            db.select(Vartotojas).where(
                Vartotojas.vaidmuo == "Dėstytojas",
                Vartotojas.dest_pat == False
            )
        ).scalars().all()
        
        return render_template('admin_destytoju_patvirtinimas.html', destytojai=destytojai)
    
    @app.route('/admin/destytojai/patvirtinti/<int:id>')
    @flask_login.login_required
    @admin_required
    def admin_patvirtinti_destytoja(id):
        try:
            admin_actions.patvirtinti_destytoja(id)
            flash("Dėstytojas sėkmingai patvirtintas", "success")
        except Exception as e:
            flash(f"Klaida patvirtinant dėstytoją: {str(e)}", "danger")
        
        return redirect(url_for('admin_destytoju_patvirtinimas'))
    
    # Modulių valdymo maršrutai
    @app.route('/admin/moduliai')
    @flask_login.login_required
    @admin_required
    def admin_moduliai():
        # Tai būtų pradinis šablonas, kurį reikėtų išplėsti su tikrais duomenimis
        return render_template('admin_moduliai.html', moduliai=[])
    
    # Studijų programų valdymo maršrutai
    @app.route('/admin/studiju-programos')
    @flask_login.login_required
    @admin_required
    def admin_studiju_programos():
        # Tai būtų pradinis šablonas, kurį reikėtų išplėsti su tikrais duomenimis
        return render_template('admin_studiju_programos.html', programos=[])
    
    # Grupių valdymo maršrutai
    @app.route('/admin/grupes')
    @flask_login.login_required
    @admin_required
    def admin_grupes():
        # Tai būtų pradinis šablonas, kurį reikėtų išplėsti su tikrais duomenimis
        return render_template('admin_grupes.html', grupes=[])