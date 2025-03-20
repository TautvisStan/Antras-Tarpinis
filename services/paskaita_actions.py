from models.paskaita import Paskaita
from extensions import db

def view_paskaitos():
    paskaitos = db.session.execute(db.select(Paskaita)).scalars().all()
    return paskaitos

def view_paskaita(id):
    paskaita = db.session.get(Paskaita, id)
    return paskaita

def sukurti_paskaita(pavadinimas, savaites_diena, laikas_nuo, laikas_iki, modulis_id):
    paskaita = Paskaita(pavadinimas = pavadinimas, savaites_diena = savaites_diena, laikas_nuo = laikas_nuo, laikas_iki = laikas_iki, modulis_id = modulis_id)
    db.session.add(paskaita)
    db.session.commit()

def gauti_paskaita(id):
    paskaita = db.session.get(Paskaita, id)
    return paskaita

def atnaujinti_paskaita(paskaita, pavadinimas, savaites_diena, laikas_nuo, laikas_iki, modulis_id):
    paskaita.pavadinimas = pavadinimas
    paskaita.savaites_diena = savaites_diena
    paskaita.laikas_nuo = laikas_nuo
    paskaita.laikas_iki = laikas_iki
    paskaita.modulis_id = modulis_id
    db.session.commit()

def salinti_paskaita(id):
    paskaita = db.session.get(Paskaita, id)
    db.session.delete(paskaita)
    db.session.commit()