from models.vartotojas import Vartotojas
from extensions import db

def view_vartotojas():
    vartotojai = db.session.execute(db.select(Vartotojas)).scalars().all()
    return vartotojai