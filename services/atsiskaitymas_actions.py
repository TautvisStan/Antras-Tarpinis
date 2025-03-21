from extensions import db
from models.atsiskaitymas import Atsiskaitymas

def view_atsiskaitymai():
    """Grąžina visų atsiskaitymų sąrašą."""
    atsiskaitymai = db.session.execute(db.select(Atsiskaitymas)).scalars().all()
    return atsiskaitymai

def sukurti_atsiskaityma(pavadinimas, data_nuo, data_iki, aprasymas, modulis_id):
    """Sukuria naują atsiskaitymą ir įrašo jį į duomenų bazę."""
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

def gauti_atsiskaityma(id):
    """Grąžina atsiskaitymą pagal nurodytą ID arba None, jei nerasta."""
    return db.session.get(Atsiskaitymas, id)

def salinti_atsiskaityma(id):
    """Pašalina atsiskaitymą pagal nurodytą ID."""
    atsiskaitymas = db.session.get(Atsiskaitymas, id)
    if atsiskaitymas:
        db.session.delete(atsiskaitymas)
        db.session.commit()
    else:
        raise ValueError(f"Atsiskaitymas su ID {id} nerastas")

def atnaujinti_atsiskaityma(atsiskaitymas, pavadinimas, data_nuo, data_iki, aprasymas, modulis_id):
    """Atnaujina esamą atsiskaitymą su pateiktais duomenimis."""
    if atsiskaitymas:
        atsiskaitymas.pavadinimas = pavadinimas
        atsiskaitymas.data_nuo = data_nuo
        atsiskaitymas.data_iki = data_iki
        atsiskaitymas.aprasymas = aprasymas
        atsiskaitymas.modulis_id = modulis_id
        db.session.commit()
    else:
        raise ValueError("Atsiskaitymas neegzistuoja")