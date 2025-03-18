from extensions import login_manager, db
from models.vartotojas import Vartotojas
from sqlalchemy import select

from services.prisijunges_actions import Prisijunges
@login_manager.user_loader
def user_loader(id):
    vartotojas = db.session.execute(db.select(Vartotojas).filter(Vartotojas.id == id)).scalars().one_or_none()
    if vartotojas is None:
        return
    prisijunges = Prisijunges()
    prisijunges.id = vartotojas.id
    return prisijunges

@login_manager.request_loader
def request_loader(request): #TODO
    email = request.form.get('email')
    vartotojas = db.session.execute(db.select(Vartotojas).filter(Vartotojas.el_pastas == email)).scalars().one_or_none()
    if vartotojas is None:
        return

    prisijunges = Prisijunges()
    prisijunges.id = vartotojas.id
    return prisijunges

def rasti_vartotoja(email, pwd): #TODO
    vartotojas = db.session.execute(db.select(Vartotojas).filter(Vartotojas.el_pastas == email and Vartotojas.password_hash == pwd)).scalars().one_or_none()
    return vartotojas