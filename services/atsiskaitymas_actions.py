from models.atsiskaitymas import Atsiskaitymas
from extensions import db

def view_atsiskaitymas():
    atsiskaitymas = db.session.execute(db.select(Atsiskaitymas)).scalars().all()
    return atsiskaitymas