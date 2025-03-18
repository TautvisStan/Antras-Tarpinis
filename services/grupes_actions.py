from models.grupes import Grupe
from extensions import db

def view_grupes():
    grupes = db.session.execute(db.select(Grupe)).scalars().all()
    return grupes