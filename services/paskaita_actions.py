from models.paskaita import Paskaita
from extensions import db

def view_paskaitos():
    paskaitos = db.session.execute(db.select(Paskaita)).scalars().all()
    return paskaitos