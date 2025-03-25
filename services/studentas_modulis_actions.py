from models.studentai_moduliai import StudentasModulis
from extensions import db

def sukurti_studento_modulius(studento_id, modulis_id):
    try:
        studentas_modulis = StudentasModulis(studentas_id=studento_id, modulis_id=modulis_id)
        db.session.add(studentas_modulis)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise Exception("Klaida priskiriant modulius studentui.")
    
def gauti_studento_modulius(studento_id):
    try:
        return db.session.execute(
            db.select(StudentasModulis).filter(StudentasModulis.studentas_id == studento_id)
        ).scalars().all()
    except Exception:
        raise Exception("Klaida gaunant studento modulius.")