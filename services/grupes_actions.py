from models.grupes import Grupe
from extensions import db

def view_grupes():
    grupes = db.session.execute(db.select(Grupe)).scalars().all()
    return grupes

def gauti_grupe(id):
    grupe = db.session.get(Grupe, id)
    return grupe

def atnaujinti_grupe(grupe, pavadinimas):
    grupe.pavadinimas = pavadinimas
    db.session.commit()

def salinti_grupe(id):
    grupe = db.session.get(Grupe, id)
    db.session.delete(grupe)
    db.session.commit()

def sukurti_grupe(pavadinimas):
    grupe = Grupe(pavadinimas=pavadinimas)
    db.session.add(grupe)
    db.session.commit()