from models.modulis import Modulis
from extensions import db

def view_modulis():
    moduliai = db.session.execute(db.select(Modulis)).scalars().all()
    return moduliai