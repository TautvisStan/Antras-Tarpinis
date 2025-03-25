from extensions import db
from models.vartotojas import Vartotojas
from models.paskaita import Paskaita
from models.atsiskaitymas import Atsiskaitymas
from models.kalendorius import Kalendorius
from datetime import datetime, timedelta
from config import Config

def gauti_vartotoja(id):
    #  Grąžina vartotoją pagal ID.
    try:
        return db.session.get(Vartotojas, id)
    except Exception as e:
        raise Exception(f"Nepavyko gauti vartotojo pagal ID: {str(e)}")

def gauti_vartotojo_tvarkarasti(vartotojas):
    # Grąžina studento tvarkaraštį: paskaitas, atsiskaitymus, egzaminus ir šventes.
    try:
        # Patikriname vartotojo vaidmenį (ignoruojame didžiąsias/mažąsias raides)
        if not vartotojas or vartotojas.vaidmuo.lower() != 'studentas':
            raise ValueError("Studentas nerastas arba neturi studento vaidmens")
        
        # Semestro datos iš konfiguracijos
        semestro_pradzia = Config.SEMESTRO_PRADZIA
        semestro_pabaiga = Config.SEMESTRO_PABAIGA

        # Patikriname, ar semestro datos yra tinkamo formato
        if not isinstance(semestro_pradzia, datetime) or not isinstance(semestro_pabaiga, datetime):
            raise ValueError("Semestro datos turi būti datetime formato")
        
        # Šventinės dienos
        sventes = db.session.execute(db.select(Kalendorius)).scalars().all()
        sventes_list = [
            {'data': svente.data, 'aprasas': svente.aprasas}
            for svente in sventes
            if svente.data is not None  # Filtruojame, jei data yra None
            ]
        sventes_datos = {svente.data for svente in sventes}
        
        paskaitos = []
        atsiskaitymai = []
        egzaminai = []

        # Patikriname, ar vartotojas turi modulių
        if not vartotojas.moduliai:
            return {
                'paskaitos': [],
                'atsiskaitymai': [],
                'egzaminai': [],
                'sventes': sorted(sventes_list, key=lambda x: x['data'])
            }

        for modulis in vartotojas.moduliai:
            # Paskaitos su filtravimu pagal šventes
            for paskaita in modulis.paskaitos:
                # Patikriname, ar savaites_diena yra tinkama
                if not hasattr(paskaita, 'savaites_diena') or paskaita.savaites_diena is None:
                    continue  # Praleidžiame, jei savaites_diena nėra

                current_date = semestro_pradzia
                while current_date <= semestro_pabaiga:
                    # Patikriname, ar diena atitinka savaites_diena (1 = pirmadienis, 7 = sekmadienis)
                    if current_date.weekday() + 1 == paskaita.savaites_diena:
                        if current_date.date() not in sventes_datos:
                            # Patikriname, ar laikas_nuo ir laikas_iki egzistuoja
                            laikas_nuo = paskaita.laikas_nuo if paskaita.laikas_nuo else "00:00"
                            laikas_iki = paskaita.laikas_iki if paskaita.laikas_iki else "00:00"
                            paskaitos.append({
                                'pavadinimas': paskaita.pavadinimas,
                                'data': current_date,
                                'laikas_nuo': paskaita.laikas_nuo,
                                'laikas_iki': paskaita.laikas_iki,
                                'modulis': modulis.pavadinimas
                            })
                    current_date += timedelta(days=1)
            
            # Atsiskaitymai
            for atsiskaitymas in modulis.atsiskaitymai:
                if atsiskaitymas.date:  # Tikriname, ar data egzistuoja
                    atsiskaitymai.append(atsiskaitymas)
            
            # Egzaminai
            if modulis.egzaminas_data:
                egzaminai.append({
                    'modulis': modulis.pavadinimas or "Neįvardintas modulis",
                    'data': modulis.egzaminas_data
                })
        
        # Rūšiuojame rezultatus
        return {
            'paskaitos': sorted(
                paskaitos,
                key=lambda x: (x['data'], x['laikas_nuo'] if x['laikas_nuo'] else "00:00")
            ),
            'atsiskaitymai': sorted(
                atsiskaitymai,
                key=lambda x: x.date if x.date else datetime.min
            ),
            'egzaminai': sorted(
                egzaminai,
                key=lambda x: x['data'] if x['data'] else datetime.min
            ),
            'sventes': sorted(sventes_list, key=lambda x: x['data'])
        }
    except Exception as e:
        raise Exception(f"Klaida bandant gauti tvarkaraštį: {str(e)}")