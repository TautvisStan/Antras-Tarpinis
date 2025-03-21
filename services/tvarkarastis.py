from extensions import db
from models.vartotojas import Vartotojas
from models.paskaita import Paskaita
from models.atsiskaitymas import Atsiskaitymas
from models.kalendorius import Kalendorius
from datetime import datetime, timedelta
from config import Config

def gauti_vartotoja(id):
    """Grąžina vartotoją pagal ID."""
    return db.session.get(Vartotojas, id)

def gauti_vartotojo_tvarkarasti(vartotojas):
    """Grąžina studento tvarkaraštį: paskaitas, atsiskaitymus, egzaminus ir šventes."""
    if not vartotojas or vartotojas.vaidmuo != 'Studentas':
        raise ValueError("Studentas nerastas arba neturi studento vaidmens")
    
    # Semestro datos iš konfiguracijos
    semestro_pradzia = Config.SEMESTRO_PRADZIA
    semestro_pabaiga = Config.SEMESTRO_PABAIGA
    
    # Šventinės dienos
    sventes = db.session.execute(db.select(Kalendorius)).scalars().all()
    sventes_list = [{'data': svente.data, 'aprasas': svente.aprasas} for svente in sventes]
    sventes_datos = {svente.data for svente in sventes}
    
    paskaitos = []
    atsiskaitymai = []
    egzaminai = []
    
    for modulis in vartotojas.moduliai:
        # Paskaitos su filtravimu pagal šventes
        for paskaita in modulis.paskaitos:
            current_date = semestro_pradzia
            while current_date <= semestro_pabaiga:
                if current_date.weekday() + 1 == paskaita.savaites_diena:
                    if current_date.date() not in sventes_datos:
                        paskaitos.append({
                            'pavadinimas': paskaita.pavadinimas,
                            'data': current_date,
                            'laikas_nuo': paskaita.laikas_nuo,
                            'laikas_iki': paskaita.laikas_iki,
                            'modulis': modulis.pavadinimas
                        })
                current_date += timedelta(days=1)
        
        # Atsiskaitymai
        atsiskaitymai.extend(modulis.atsiskaitymai)
        
        # Egzaminai
        if modulis.egzaminas_data:
            egzaminai.append({
                'modulis': modulis.pavadinimas,
                'data': modulis.egzaminas_data
            })
    
    return {
        'paskaitos': sorted(paskaitos, key=lambda x: (x['data'], x['laikas_nuo'])),
        'atsiskaitymai': sorted(atsiskaitymai, key=lambda x: x.data),
        'egzaminai': sorted(egzaminai, key=lambda x: x['data']),
        'sventes': sorted(sventes_list, key=lambda x: x['data'])
    }