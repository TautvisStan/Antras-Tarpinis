from datetime import datetime, timedelta
from flask import render_template
from .models import Paskaita, Kalendorius

def init_tvarkarastis():
    @app.route('/tvarkarastis')
    def tvarkarastis():
        savaites_shift = int(request.args.get('savaites_shift', 0))  # Savaitės poslinkis
        savaites_pradzia = datetime.now() + timedelta(weeks=savaites_shift) - timedelta(days=datetime.now().weekday())
        savaites_pabaiga = savaites_pradzia + timedelta(days=4)  # Tik darbo dienos

        # Filtruojame paskaitas šiai savaitei
        paskaitos = Paskaita.query.filter(
            Paskaita.pradzia >= savaites_pradzia,
            Paskaita.pabaiga <= savaites_pabaiga
        ).all()

        # Filtruojame šventines/išeigines dienas
        sventines_dienos = Kalendorius.query.filter(
            Kalendorius.data >= savaites_pradzia.date(),
            Kalendorius.data <= savaites_pabaiga.date()
        ).all()

        # Grupuojame paskaitas pagal dieną ir laiką
        tvarkarastis = {
            'pirmadienis': {}, 'antradienis': {}, 'trečiadienis': {}, 'ketvirtadienis': {}, 'penktadienis': {}
        }
        laiko_intervalai = set()

        for paskaita in paskaitos:
            diena = paskaita.pradzia.strftime('%A').lower()  # Gauti dieną (pvz., 'pirmadienis')
            laikas = paskaita.pradzia.strftime('%H:%M')  # Paskaitos pradžios laikas

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
        sventine_diena = Kalendorius.query.filter_by(data=data.date()).first()
        return sventine_diena is None

    # pakaitos pridejimas su tikrinimu

    # Prieš įtraukiant paskaitą į tvarkaraštį, reikia patikrinti, ar diena nėra šventinė/išeiginė:

    @app.route('/prideti_paskaita', methods=['POST'])
    @login_required
    def prideti_paskaita():
        if current_user.vaidmuo != 'Dėstytojas':
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
        if current_user.vaidmuo != 'Dėstytojas':
            flash('Neturite teisių šalinti paskaitų', 'danger')
            return redirect(url_for('tvarkarastis'))

        paskaita = Paskaita.query.get_or_404(id)
        db.session.delete(paskaita)
        db.session.commit()
        flash('Paskaita sėkmingai pašalinta', 'success')
        return redirect(url_for('tvarkarastis'))
