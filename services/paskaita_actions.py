from models.paskaita import Paskaita
from extensions import db

def view_paskaitos():
    try:
        paskaitos = db.session.execute(db.select(Paskaita)).scalars().all()
        return paskaitos
    except Exception:
        raise Exception("Klaida bandant gauti paskaitas.")

def view_paskaita(id):
    try:
        paskaita = db.session.get(Paskaita, id)
        return paskaita
    except Exception:
        raise Exception("Klaida bandant gauti paskaitą.")

def sukurti_paskaita(pavadinimas, savaites_diena, laikas_nuo, laikas_iki, modulis_id):
    try:
        paskaita = Paskaita(pavadinimas = pavadinimas, savaites_diena = savaites_diena, laikas_nuo = laikas_nuo, laikas_iki = laikas_iki, modulis_id = modulis_id)
        db.session.add(paskaita)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise Exception("Klaida bandant sukurti paskaitą.")

def gauti_paskaita(id):
    try:
        paskaita = db.session.get(Paskaita, id)
        return paskaita
    except Exception:
        raise Exception("Klaida bandant gauti paskaitą.")

def atnaujinti_paskaita(paskaita, pavadinimas, savaites_diena, laikas_nuo, laikas_iki, modulis_id):
    try:
        paskaita.pavadinimas = pavadinimas
        paskaita.savaites_diena = savaites_diena
        paskaita.laikas_nuo = laikas_nuo
        paskaita.laikas_iki = laikas_iki
        paskaita.modulis_id = modulis_id
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise Exception("Klaida bandant atnaujinti paskaitą.")

def salinti_paskaita(id):
    try:
        paskaita = db.session.get(Paskaita, id)
        if paskaita:
            db.session.delete(paskaita)
            db.session.commit()
        else:
            raise Exception("Paskaita nerasta.")
    except Exception:
        db.session.rollback()
        raise Exception("Klaida bandant pašalinti paskaitą.")
