from models.modulis import Modulis
from extensions import db

def view_modulis():
    moduliai = db.session.execute(db.select(Modulis)).scalars().all()
    return moduliai

def gauti_moduli(id):
    modulis = db.session.get(Modulis, id)
    return modulis

def atnaujinti_moduli(modulis, pavadinimas, aprasymas, kreditai, semestro_informacija, studiju_programa, destytojas):
    modulis.pavadinimas = pavadinimas
    modulis.aprasymas = aprasymas
    modulis.kreditai = kreditai
    modulis.semestro_informacija = semestro_informacija
    db.session.commit()
    if studiju_programa:
        modulis.studiju_programa_id = studiju_programa.id

    if destytojas:
        modulis.destytojas_id = destytojas.id

    db.session.commit()

def salinti_moduli(id):
    modulis = db.session.get(Modulis, id)
    db.session.delete(modulis)
    db.session.commit()

def sukurti_moduli(pavadinimas, aprasymas, kreditai, semestro_informacija, destytojas_id, studiju_programa):
    modulis = Modulis(pavadinimas=pavadinimas, aprasymas=aprasymas, kreditai=kreditai, semestro_informacija=semestro_informacija, destytojas_id=destytojas_id, studiju_programa=studiju_programa)
    db.session.add(modulis)
    db.session.commit()

