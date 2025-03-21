from models.atsiskaitymas import Atsiskaitymas
from extensions import db
from models.modulis import Modulis

def view_atsiskaitymas():
    atsiskaitymas = db.session.execute(db.select(Atsiskaitymas)).scalars().all()
    return atsiskaitymas

def priskirti_atsiskaityma_moduliui(data, aprasymas, modulis_id):
    modulis = db.session.execute(db.select(Modulis).filter(Modulis.id == modulis_id)).scalar_one_or_none()
    if not modulis:
        raise Exception("Modulis nerastas")
    
    atsiskaitymas = Atsiskaitymas(data=data, aprasymas=aprasymas, modulis_id=modulis_id)
    db.session.add(atsiskaitymas)
    db.session.commit()

    return atsiskaitymas

def gauti_atsiskaitymus(modulis_id):
    return db.session.execute(
        db.select(Atsiskaitymas).filter(Atsiskaitymas.modulis_id == modulis_id)
    ).scalars().all()