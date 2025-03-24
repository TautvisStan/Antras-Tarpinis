from models.modulis import Modulis
from models.paskaita import Paskaita
from extensions import db
from sqlalchemy import select

def view_modulis():
    # Grąžina visų modulių sąrašą.
    try:
        moduliai = db.session.execute(select(Modulis)).scalars().all()
        return moduliai
    except Exception as e:
        raise Exception(f"Klaida gaunant modulius: {str(e)}")

def gauti_moduli(id):
    # Grąžina modulį pagal ID.
    try:
        modulis = db.session.execute(select(Modulis).where(Modulis.id == id)).scalars().first()
        if not modulis:
            raise Exception(f"Modulis su ID {id} nerastas")
        return modulis
    except Exception as e:
        raise Exception(f"Klaida gaunant modulį: {str(e)}")

def atnaujinti_moduli(modulis, pavadinimas, aprasymas, kreditai, semestro_informacija, egzaminas_data, paskaita_data_list):
    # Atnaujina modulį ir susijusią paskaitą.
    try:
        modulis.pavadinimas = pavadinimas
        modulis.aprasymas = aprasymas
        modulis.kreditai = kreditai
        modulis.semestro_informacija = semestro_informacija
        modulis.egzaminas_data = egzaminas_data
        
        # Pašaliname senas paskaitas
        for paskaita in modulis.paskaitos:
            db.session.delete(paskaita)
        
        # Pridedame naujas paskaitas
        for paskaita_data in paskaita_data_list:
            paskaita = Paskaita(
                pavadinimas=paskaita_data['pavadinimas'],
                savaites_diena=paskaita_data['savaites_diena'],
                laikas_nuo=paskaita_data['laikas_nuo'],
                laikas_iki=paskaita_data['laikas_iki'],
                modulis=modulis
            )
            db.session.add(paskaita)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Modulio atnaujinimo klaida: {str(e)}")

def salinti_moduli(id):
    # Pašalina modulį pagal ID.
    try:
        modulis = db.session.execute(select(Modulis).where(Modulis.id == id)).scalars().first()
        if modulis:
            db.session.delete(modulis)
            db.session.commit()
        else:
            raise Exception(f"Modulis su ID {id} nerastas")
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Modulio šalinimo klaida: {str(e)}")

def sukurti_moduli(pavadinimas, aprasymas, kreditai, semestro_informacija, destytojas_id, studiju_programa_id, egzaminas_data, paskaita_data):
    # Sukuria naują modulį ir susijusią paskaitą.
    try:
        modulis = Modulis(
            pavadinimas=pavadinimas,
            aprasymas=aprasymas,
            kreditai=kreditai,
            semestro_informacija=semestro_informacija,
            destytojas_id=destytojas_id,
            studiju_programa_id=studiju_programa_id,
            egzaminas_data=egzaminas_data
        )
        paskaita = Paskaita(
            pavadinimas=paskaita_data['pavadinimas'],
            savaites_diena=paskaita_data['savaites_diena'],
            laikas_nuo=paskaita_data['laikas_nuo'],
            laikas_iki=paskaita_data['laikas_iki'],
            modulis=modulis
        )
        db.session.add(modulis)
        db.session.add(paskaita)
        db.session.commit()
        return modulis
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Modulio sukūrimo klaida: {str(e)}")
