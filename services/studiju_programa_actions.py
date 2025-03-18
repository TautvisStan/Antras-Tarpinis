from models.studiju_programa import StudijuPrograma
from extensions import db

def view_studiju_programa():
    studiju_programa = db.session.execute(db.select(StudijuPrograma)).scalars().all()
    return studiju_programa

def gauti_studiju_programa(id):
    studiju_programa = db.session.get(StudijuPrograma, id)
    return studiju_programa

def atnaujinti_studiju_programa(studiju_programa, pavadinimas):
    studiju_programa.pavadinimas = pavadinimas
    db.session.commit()

def salinti_studiju_programa(id):
    studiju_programa = db.session.get(StudijuPrograma, id)
    db.session.delete(studiju_programa)
    db.session.commit()

def sukurti_studiju_programa(pavadinimas):
    studiju_programa = StudijuPrograma(pavadinimas=pavadinimas)
    db.session.add(studiju_programa)
    db.session.commit()