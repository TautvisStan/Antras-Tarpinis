from extensions import db
from models.studiju_programa import StudijuPrograma
from models.grupes import Grupe
from models.vartotojas import Vartotojas
from datetime import datetime
from sqlalchemy import func


def sukurti_grupes_pavadinima(id):
    try:
        programa = db.session.get(StudijuPrograma,id)

        if not programa:
            raise Exception("Studijų programa nerasta.")

        pavadinimo_trumpinys = ''.join(zodis[0].upper() for zodis in programa.pavadinimas.split())

        metu_trumpinys = str(datetime.now().year)[-2:]

        esamos_grupes = db.session.execute(db.select(Grupe).filter_by(studiju_programa_id = programa.id)).scalars().all()

        grupiu_skaicius = len(esamos_grupes)

        grupes_raide = chr(65 + grupiu_skaicius)

        pavadinimas = f"{pavadinimo_trumpinys}{metu_trumpinys}{grupes_raide}"

        return pavadinimas
    except Exception:
        print("Klaida kuriant grupės pavadinimą.")
        return None


def automatiskai_priskirti_grupe(vartotojas):
    while True:
        try:
            paskutine_grupe = db.session.execute(db.select(Grupe).filter(Grupe.studiju_programa_id == vartotojas.studiju_programa_id).order_by(Grupe.id.desc())).scalars().first()

            if not paskutine_grupe:
                pirmos_grupes_pavadinimas = sukurti_grupes_pavadinima(vartotojas.studiju_programa_id)
                pirma_grupe = Grupe(pavadinimas = pirmos_grupes_pavadinimas,studiju_programa_id = vartotojas.studiju_programa_id )
                db.session.add(pirma_grupe)
                db.session.commit()
        
                vartotojas.grupe_id = pirma_grupe.id
                db.session.commit()
                return

            studentu_skaicius = db.session.execute(db.select(func.count()).filter(Vartotojas.grupe_id == paskutine_grupe.id)).scalar() or 0

            if studentu_skaicius < 30:
                vartotojas.grupe_id = paskutine_grupe.id
                db.session.commit()
                return
            
            grupe1_pavadinimas = sukurti_grupes_pavadinima(paskutine_grupe.studiju_programa_id)
            grupe2_pavadinimas = sukurti_grupes_pavadinima(paskutine_grupe.studiju_programa_id)

            grupe1 = Grupe(pavadinimas = grupe1_pavadinimas,studiju_programa_id = vartotojas.studiju_programa_id )
            grupe2 = Grupe(pavadinimas = grupe2_pavadinimas,studiju_programa_id = vartotojas.studiju_programa_id )

            db.session.add(grupe1)
            db.session.add(grupe2)
            db.session.commit()
        
            studentai_senoje_grupeje = db.session.execute(db.select(Vartotojas).filter(Vartotojas.grupe_id == paskutine_grupe.id)).scalars().all()

            for i, studentas in enumerate(studentai_senoje_grupeje):
                if i < 15:
                    studentas.grupe_id = grupe1.id
                else:
                    studentas.grupe_id = grupe2.id
            db.session.commit()
        except Exception:
            db.session.rollback()
            print("Klaida bandant priskirti grupę.")
            return










