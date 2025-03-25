from models.studiju_programa import StudijuPrograma
from models.specializacija import Specializacija
from extensions import db

def view_studiju_programa():
    try:
        studiju_programa = db.session.execute(db.select(StudijuPrograma)).scalars().all()
        return studiju_programa
    except Exception:
        raise Exception ("Klaida bandant gauti studiju programas.")

def gauti_studiju_programa(id):
    try:
        studiju_programa = db.session.get(StudijuPrograma, id)
        return studiju_programa
    except Exception:
        raise Exception ("Klaida bandant gauti studijų programą.")

def atnaujinti_studiju_programa(studiju_programa, pavadinimas):
    try:
        studiju_programa.pavadinimas = pavadinimas
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise Exception ("Klaida bandant atnaujinti studijų programą.")

def salinti_studiju_programa(id):
    try:
        studiju_programa = db.session.get(StudijuPrograma, id)
        if not studiju_programa:
            raise Exception ("Studijų prorama nerasta.")
        db.session.delete(studiju_programa)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise Exception ("Klaida bandant pašalinti studijų programą.")

def sukurti_studiju_programa(pavadinimas,specializacija_id):
    try:
        studiju_programa = StudijuPrograma(pavadinimas=pavadinimas,specializacija_id=specializacija_id)
        db.session.add(studiju_programa)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise Exception ("Klaida bandant sukurti studijų programą.")