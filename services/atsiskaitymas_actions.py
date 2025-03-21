from extensions import db
from models.atsiskaitymas import Atsiskaitymas
from models.modulis import Modulis

def view_atsiskaitymai():
    """Grąžina visų atsiskaitymų sąrašą."""
    try:
        atsiskaitymai = db.session.execute(db.select(Atsiskaitymas)).scalars().all()
        return atsiskaitymai
    except Exception:
        raise Exception("Klaida bandant gauti atsiskaitymus")

def sukurti_atsiskaityma(pavadinimas, data_nuo, data_iki, aprasymas, modulis_id):
    """Sukuria naują atsiskaitymą ir įrašo jį į duomenų bazę."""
    try:
        atsiskaitymas = Atsiskaitymas(
            pavadinimas=pavadinimas,
            data_nuo=data_nuo,
            data_iki=data_iki,
            aprasymas=aprasymas,
            modulis_id=modulis_id
        )
        db.session.add(atsiskaitymas)
        db.session.commit()
        return atsiskaitymas
    except Exception:
        db.session.rollback()
        raise Exception ("Klaida bandant sukurti atsiskaitymą")

def gauti_atsiskaityma(id):
    """Grąžina atsiskaitymą pagal nurodytą ID arba None, jei nerasta."""
    try:
        atsiskaitymas =db.session.get(Atsiskaitymas, id)
        return atsiskaitymas
    except Exception:
        db.session.rollback()
        raise Exception ("Klaida bandant gauti atsiskaitymą.")

def salinti_atsiskaityma(id):
    """Pašalina atsiskaitymą pagal nurodytą ID."""
    try:
        atsiskaitymas = db.session.get(Atsiskaitymas, id)
        if atsiskaitymas:
            db.session.delete(atsiskaitymas)
            db.session.commit()
        else:
            raise ValueError(f"Atsiskaitymas su ID {id} nerastas")
    except Exception:
        db.session.rollback()
        raise Exception ("Klaida šalinant atsiskaitymą")

def atnaujinti_atsiskaityma(atsiskaitymas, pavadinimas, data_nuo, data_iki, aprasymas, modulis_id):
    """Atnaujina esamą atsiskaitymą su pateiktais duomenimis."""
    try:
        if not atsiskaitymas:
            raise Exception ("Atsiskaitymas neegzistuoja")
        atsiskaitymas.pavadinimas = pavadinimas
        atsiskaitymas.data_nuo = data_nuo
        atsiskaitymas.data_iki = data_iki
        atsiskaitymas.aprasymas = aprasymas
        atsiskaitymas.modulis_id = modulis_id
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise Exception("Klaida atnaujinant atsiskaitymą.")

def view_atsiskaitymas():
    try:
        atsiskaitymas = db.session.execute(db.select(Atsiskaitymas)).scalars().all()
        return atsiskaitymas
    except Exception:
        db.session.rollback()
        raise Exception("Klaida gaunant atsiskaitymus.")

def priskirti_atsiskaityma_moduliui(data, aprasymas, modulis_id):
    try:
        modulis = db.session.execute(db.select(Modulis).filter(Modulis.id == modulis_id)).scalar_one_or_none()
        if not modulis:
            raise Exception("Modulis nerastas")
        
        atsiskaitymas = Atsiskaitymas(data=data, aprasymas=aprasymas, modulis_id=modulis_id)
        db.session.add(atsiskaitymas)
        db.session.commit()

        return atsiskaitymas
    except Exception:
        db.session.rollback()
        raise Exception("Klaida priskiriant atsiskaitymą.")

def gauti_atsiskaitymus(modulis_id):
    try:
        return db.session.execute(
            db.select(Atsiskaitymas).filter(Atsiskaitymas.modulis_id == modulis_id)
        ).scalars().all()
    except Exception:
        raise Exception("Klaida gaunant atsiskaitymus pagal modulį.")
