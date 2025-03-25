# from datetime import datetime
# from extensions import db
# from models.vartotojas import Vartotojas
# from models.modulis import Modulis
# from models.grupes import Grupe
# from models.studiju_programa import StudijuPrograma

# def gauti_statistika():
#     vartotoju_skaicius = db.session.execute(db.select(db.func.count()).select_from(Vartotojas)).scalar()
#     moduliu_skaicius = db.session.execute(db.select(db.func.count()).select_from(Modulis)).scalar()
#     studiju_programu_skaicius = db.session.execute(db.select(db.func.count()).select_from(StudijuPrograma)).scalar()
#     grupiu_skaicius = db.session.execute(db.select(db.func.count()).select_from(Grupe)).scalar()

#     vartotoju_skaicius = vartotoju_skaicius if vartotoju_skaicius is not None else 0
#     moduliu_skaicius = moduliu_skaicius if moduliu_skaicius is not None else 0
#     studiju_programu_skaicius = studiju_programu_skaicius if studiju_programu_skaicius is not None else 0
#     grupiu_skaicius = grupiu_skaicius if grupiu_skaicius is not None else 0

#     return vartotoju_skaicius,moduliu_skaicius,studiju_programu_skaicius,grupiu_skaicius 

# def gauti_vartotojus():
#     vartotojai = db.session.execute(db.select(Vartotojas)).scalars().all()
#     return vartotojai

# def sukurti_vartotoja(vardas,pavarde,vaidmuo,el_pastas,password_hash):
#     vartotojas = Vartotojas(vardas=vardas, pavarde=pavarde, vaidmuo=vaidmuo, el_pastas=el_pastas, password_hash=password_hash)
#     db.session.add(vartotojas)
#     db.session.commit()

# def gauti_vartotoja(id):
#     vartotojas = db.session.get(Vartotojas, id)
#     return vartotojas

# def redaguoti_vartotoja(vartotojas,vardas,pavarde,vaidmuo):
#     vartotojas.vardas = vardas
#     vartotojas.pavarde = pavarde
#     vartotojas.vaidmuo = vaidmuo
#     db.session.commit()

# def istrinti_vartotoja(id):
#     vartotojas = db.session.get(Vartotojas, id)
#     db.session.delete(vartotojas)
#     db.session.commit()

# # def istrinti_vartotoja(vartotojas):
# #     try:
# #         db.session.delete(vartotojas)
# #         db.session.commit()  
# #     except Exception as e:
# #         db.session.rollback()  
# #         raise Exception(f"Klaida trinant vartotoją: {e}")
    
# def uzblokuoti_vartotoja(vartotojas):
#     try:
#         vartotojas.aktyvumas = False
#         db.session.commit()  
#     except Exception as e:
#         db.session.rollback()  
#         raise Exception(f"Klaida užblokuojant vartotoją: {e}")

# def patvirtinti_destytoja(id):
#     destytojas = db.session.get(Vartotojas, id)
#     destytojas.dest_pat = True
#     destytojas.dest_pat_data = datetime.now()
#     db.session.commit()

from datetime import datetime
from extensions import db
from models.vartotojas import Vartotojas
from models.modulis import Modulis
from models.grupes import Grupe
from models.studiju_programa import StudijuPrograma

def gauti_statistika():
    try:
        vartotoju_skaicius = db.session.execute(db.select(db.func.count()).select_from(Vartotojas)).scalar()
        moduliu_skaicius = db.session.execute(db.select(db.func.count()).select_from(Modulis)).scalar()
        studiju_programu_skaicius = db.session.execute(db.select(db.func.count()).select_from(StudijuPrograma)).scalar()
        grupiu_skaicius = db.session.execute(db.select(db.func.count()).select_from(Grupe)).scalar()

        vartotoju_skaicius = vartotoju_skaicius if vartotoju_skaicius is not None else 0
        moduliu_skaicius = moduliu_skaicius if moduliu_skaicius is not None else 0
        studiju_programu_skaicius = studiju_programu_skaicius if studiju_programu_skaicius is not None else 0
        grupiu_skaicius = grupiu_skaicius if grupiu_skaicius is not None else 0

        return (vartotoju_skaicius or 0,
                moduliu_skaicius or 0,
                studiju_programu_skaicius or 0,
                grupiu_skaicius or 0)
    except Exception:
        raise Exception("Klaida bandant gauti statistiką:")

def gauti_vartotojus():
    try:
        vartotojai = db.session.execute(db.select(Vartotojas)).scalars().all()
        return vartotojai
    except Exception:
        raise Exception("Klaida bandant gauti vartotojus:")

def sukurti_vartotoja(vardas,pavarde,vaidmuo,studiju_programa_id, fakultetas_id,el_pastas,password_hash):
    try:
        vartotojas = Vartotojas(vardas=vardas, pavarde=pavarde, vaidmuo=vaidmuo,studiju_programa_id=studiju_programa_id,
        fakultetas_id=fakultetas_id, el_pastas=el_pastas, password_hash=password_hash)
        db.session.add(vartotojas)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise Exception("Klaida bandant sukurti vartotoją:")

def gauti_vartotoja(id):
    try:
        vartotojas = db.session.get(Vartotojas, id)
        return vartotojas
    except Exception:
        raise Exception("Klaida bandant gauti vartotoją:")

def redaguoti_vartotoja(vartotojas,vardas,pavarde,vaidmuo):
    try:
        vartotojas.vardas = vardas
        vartotojas.pavarde = pavarde
        vartotojas.vaidmuo = vaidmuo
        db.session.commit()
    except Exception:
        db.session.rollback()
        print("Klaida redaguojant vartotoją:")

def pasalinti_vartotoja(id):
    try:
        vartotojas = db.session.get(Vartotojas, id)
        if vartotojas:
            db.session.delete(vartotojas)
            db.session.commit()
        else:
            raise Exception("Vartotojas nerastas.")
    except Exception:
        db.session.rollback()
        raise Exception("Klaida bandant ištrinti vartotoją.")


def istrinti_vartotoja(vartotojas):
    try:
        db.session.delete(vartotojas)
        db.session.commit()  
    except Exception as e:
        db.session.rollback()  
        raise Exception("Klaida trinant vartotoją.")
    
def uzblokuoti_vartotoja(vartotojas):
    """Užblokuoja vartotoją (pakeičia aktyvumo būseną į False)"""
    try:
        vartotojas.aktyvumas = False
        db.session.commit()  
    except Exception:
        db.session.rollback()  
        raise Exception("Klaida užblokuojant vartotoją:")

def patvirtinti_destytoja(id):
    try:
        destytojas = db.session.get(Vartotojas, id)
        if destytojas:
            destytojas.dest_pat = True
            destytojas.dest_pat_data = datetime.now()
            db.session.commit()
        else:
            raise Exception ("Dėstytojas nerastas.")
    except Exception:
        db.session.rollback()
        raise Exception("Klaida bandant patvirtinti dėstytoją.")
