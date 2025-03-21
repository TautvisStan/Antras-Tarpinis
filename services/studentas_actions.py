from models.vartotojas import Vartotojas
from extensions import db

def perziureti_studentus():
    try:
        studentai = db.session.execute(db.select(Vartotojas).filter(Vartotojas.vaidmuo == "Studentas")).scalars().all()
        return studentai
    except Exception:
        raise Exception("Klaida gaunant studentų sąrašą.")

def gauti_studenta(id):
    try:
        studentas = db.session.get(Vartotojas, id)
        if studentas and studentas.vaidmuo == "Studentas":
            return studentas
        else:
            raise Exception("Studentas nerastas.")
    except Exception:
        raise Exception("Klaida gaunant studento informaciją.")
