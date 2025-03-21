from models.studentai_moduliai import StudentasModulis
from extensions import db

def sukurti_studento_modulius(studento_id, pasirinkti_moduliai):
    for modulis in pasirinkti_moduliai:
        studentas_modulis = StudentasModulis(studentas_id=studento_id, modulis_id=modulis.id)
        db.session.add(studentas_modulis)
        db.session.commit()
    
def gauti_studento_modulius(studento_id):
    return db.session.execute(
        db.select(StudentasModulis).filter(StudentasModulis.studentas_id == studento_id)
    ).scalars().all()