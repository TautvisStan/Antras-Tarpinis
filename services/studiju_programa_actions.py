from models.studiju_programa import StudijuPrograma
from extensions import db

def view_studiju_programa():
    studiju_programa = db.session.execute(db.select(StudijuPrograma)).scalars().all()
    return studiju_programa