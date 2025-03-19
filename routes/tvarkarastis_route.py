from datetime import datetime, timedelta
from flask import render_template, request, redirect, url_for, flash, select
from models import Paskaita, Kalendorius, Vartotojas
from flask_login import login_required
from extensions import db


def init_tvarkarastis(app):
    @app.route('/tvarkarastis')
    def tvarkarastis():
        savaites_shift = int(request.args.get('savaites_shift', 0))  # Savaitės poslinkis
        savaites_pradzia = datetime.now() + timedelta(weeks=savaites_shift) - timedelta(days=datetime.now().weekday())
        savaites_pabaiga = savaites_pradzia + timedelta(days=4)  # Tik darbo dienos

        # Filtruojame paskaitas šiai savaitei
        stmt_paskaitos = db.session.execute(db.select(Paskaita).where(
            Paskaita.laikas_nuo >= savaites_pradzia,
            Paskaita.laikas_iki <= savaites_pabaiga
        ))
        paskaitos = db.session.execute(stmt_paskaitos).scalars().all()    
    
        # Filtruojame šventines/išeigines dienas
        stmt_sventines_dienos = db.session.execute(db.select(Kalendorius).where(
            Kalendorius.data >= savaites_pradzia.date(),
            Kalendorius.data <= savaites_pabaiga.date()
        ))
        sventines_dienos = db.session.execute(stmt_sventines_dienos).scalars().all() 

        # Grupuojame paskaitas pagal dieną ir laiką
        tvarkarastis = {
            'pirmadienis': {}, 'antradienis': {}, 'trečiadienis': {}, 'ketvirtadienis': {}, 'penktadienis': {}
        }
        laiko_intervalai = set()

        for paskaita in paskaitos:
            diena = paskaita.savaites_diena.strftime('%A').lower()  # Gauti dieną (pvz., 'pirmadienis')
            laikas = paskaita.laikas_nuo.strftime('%H:%M')  # Paskaitos pradžios laikas

            if diena in tvarkarastis:
                if laikas not in tvarkarastis[diena]:
                    tvarkarastis[diena][laikas] = []
                tvarkarastis[diena][laikas].append(paskaita)
                laiko_intervalai.add(laikas)

        # Konvertuojame laiko intervalus į sąrašą ir išrikiuojame
        laiko_intervalai = sorted(laiko_intervalai)

        return render_template('tvarkarastis.html', tvarkarastis=tvarkarastis, laiko_intervalai=laiko_intervalai,
                            savaites_pradzia=savaites_pradzia.strftime('%Y-%m-%d'),
                            savaites_pabaiga=savaites_pabaiga.strftime('%Y-%m-%d'))
        
    # sventiniu, iseiginiu dienu patikrinimas

    def ar_darbo_diena(data):
        stmt_sventine_diena = db.session.execute(db.select(Kalendorius).where(Kalendorius.data == data.date))
        sventine_diena = db.session.execute(stmt_sventine_diena).scalars().first()
        return sventine_diena is None

    # pakaitos pridejimas su tikrinimu
    # Prieš įtraukiant paskaitą į tvarkaraštį, reikia patikrinti, ar diena nėra šventinė/išeiginė:

    @app.route('/prideti_paskaita', methods=['POST'])
    @login_required
    def prideti_paskaita():
        if Vartotojas.vaidmuo != 'Dėstytojas':
            flash('Neturite teisių pridėti paskaitų', 'danger')
            return redirect(url_for('tvarkarastis'))

        modulio_id = request.form['modulio_id']
        pradzia = datetime.strptime(request.form['pradzia'], '%Y-%m-%dT%H:%M')
        pabaiga = datetime.strptime(request.form['pabaiga'], '%Y-%m-%dT%H:%M')
        vieta = request.form['vieta']

        if not ar_darbo_diena(pradzia):
            flash('Paskaita negali būti planuojama šventinėje/išeiginėje dienoje', 'danger')
            return redirect(url_for('tvarkarastis'))

        paskaita = Paskaita(modulio_id=modulio_id, pradzia=pradzia, pabaiga=pabaiga, vieta=vieta)
        db.session.add(paskaita)
        db.session.commit()
        flash('Paskaita sėkmingai pridėta', 'success')
        return redirect(url_for('tvarkarastis'))

    # paskaitos salinimas

    @app.route('/salinti_paskaita/<int:id>', methods=['POST'])
    @login_required
    def salinti_paskaita(id):
        if Vartotojas.vaidmuo != 'Dėstytojas':
            flash('Neturite teisių šalinti paskaitų', 'danger')
            return redirect(url_for('tvarkarastis'))

        paskaita = db.session.get(Paskaita, id)
        db.session.delete(paskaita)
        db.session.commit()
        flash('Paskaita sėkmingai pašalinta', 'success')
        return redirect(url_for('tvarkarastis'))
