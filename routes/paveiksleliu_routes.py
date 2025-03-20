from flask import request, flash, redirect, url_for, render_template
from models.vartotojas import Vartotojas, db
from services import issaugoti_paveiksleli
from datetime import datetime
from forms import registerForma

def inicijuoti_marsrutus(app):
    @app.route('/profilis', methods=['GET', 'POST'])
    def profilis():
        if request.method == 'POST':
            if 'profilio_pav' not in request.files:
                flash('Nera failo dalies')
                return redirect(request.url)
            
            failas = request.files['profilio_pav']
            
            if failas.filename == '':
                flash('Nepasirinktas failas')
                return redirect(request.url)
            
            try:
                vartotojas = Vartotojas.query.first()
                if not vartotojas:
                    # Pridedame bandomoji vartotoja
                    vartotojas = Vartotojas(vardas='Jonas', pavarde='Jonaitis')
                    db.session.add(vartotojas)
                    db.session.commit()
                
                failo_pavadinimas = issaugoti_paveiksleli(failas, vartotojas)
                if failo_pavadinimas:
                    vartotojas.profilio_pav = failo_pavadinimas
                    vartotojas.ikelimo_data = datetime.utcnow()
                    db.session.commit()
                    flash('Profilio foto sekmingai ikelta')
                    return redirect(url_for('profilis'))
                else:
                    flash('Netinkamas failo tipas arba dydis')
                    return redirect(request.url)
            except Exception as e:
                flash(f'Klaida ikeliant faila: {str(e)}')
                return redirect(request.url)
        
        vartotojai = Vartotojas.query.all()
        return render_template('profile.html', vartotojai=vartotojai)
    
    @app.route('/registracija', methods=['GET', 'POST'])
    def registracija():
        forma = registerForma()
        if forma.validate_on_submit():
            try:
                naujas_vartotojas = Vartotojas(
                    vardas=forma.vardas.data,
                    pavarde=forma.pavarde.data,
                    el_pastas=forma.el_pastas.data,
                    slaptazodis=forma.slaptazodis.data,
                    vaidmuo=forma.vaidmuo.data,
                    profilio_pav=forma.profilio_pav.data,
                    studiju_programa=forma.studiju_programa.data
                )
                db.session.add(naujas_vartotojas)
                db.session.commit()



                flash('Registracija sekminga')
                return redirect(url_for('profilis'))
            except Exception as e:
                flash(f'Klaida registruojant: {str(e)}')
                db.session.rollback()
        
        return render_template('registracija.html', forma=forma)

    @app.route('/')
    def pradzia():
        return redirect(url_for('profilis'))

    @app.route('/perziureti_paveiksleli/<int:vartotojo_id>')
    def perziureti_paveiksleli(vartotojo_id):
        vartotojas = Vartotojas.query.get_or_404(vartotojo_id)
        return render_template('profile.html', vartotojas=vartotojas)