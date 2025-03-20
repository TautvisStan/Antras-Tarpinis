from datetime import datetime
from extensions import db
from models.vartotojas import Vartotojas
from models.modulis import Modulis
from models.grupes import Grupe
from models.studiju_programa import StudijuPrograma

def gauti_statistika():
    vartotoju_skaicius = db.session.execute(db.select(db.func.count()).select_from(Vartotojas)).scalar()
    moduliu_skaicius = db.session.execute(db.select(db.func.count()).select_from(Modulis)).scalar()
    studiju_programu_skaicius = db.session.execute(db.select(db.func.count()).select_from(StudijuPrograma)).scalar()
    grupiu_skaicius = db.session.execute(db.select(db.func.count()).select_from(Grupe)).scalar()

    vartotoju_skaicius = vartotoju_skaicius if vartotoju_skaicius is not None else 0
    moduliu_skaicius = moduliu_skaicius if moduliu_skaicius is not None else 0
    studiju_programu_skaicius = studiju_programu_skaicius if studiju_programu_skaicius is not None else 0
    grupiu_skaicius = grupiu_skaicius if grupiu_skaicius is not None else 0

    return vartotoju_skaicius,moduliu_skaicius,studiju_programu_skaicius,grupiu_skaicius 

def istrinti_vartotoja(vartotojas):
    try:
        db.session.delete(vartotojas)
        db.session.commit()  
    except Exception as e:
        db.session.rollback()  
        raise Exception(f"Klaida trinant vartotoją: {e}")
    
def uzblokuoti_vartotoja(vartotojas):
    try:
        vartotojas.aktyvumas = False
        db.session.commit()  
    except Exception as e:
        db.session.rollback()  
        raise Exception(f"Klaida užblokuojant vartotoją: {e}")

def patvirtinti_destytoja(id):
    destytojas = db.session.get(Vartotojas, id)
    destytojas.dest_pat = True
    destytojas.dest_pat_data = datetime.now()
    db.session.commit()
