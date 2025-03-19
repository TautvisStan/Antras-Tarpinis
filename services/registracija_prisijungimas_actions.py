from extensions import login_manager, db
from models.vartotojas import Vartotojas
from sqlalchemy import select
from extensions import Prisijunges
from passlib.hash import pbkdf2_sha256

@login_manager.user_loader
def user_loader(id):
    vartotojas = db.session.execute(db.select(Vartotojas).filter(Vartotojas.id == id)).scalars().one_or_none()
    if vartotojas is None:
        return
    return prijungti_vartotoja(vartotojas)

@login_manager.request_loader
def request_loader(request): #TODO
    email = request.form.get('el_pastas')
    password = request.form.get('slaptazodis')
    vartotojas = rasti_vartotoja(email, password)
    if vartotojas:
        return prijungti_vartotoja(vartotojas)
    else:
        return
    
def prijungti_vartotoja(vartotojas):
    prisijunges = Prisijunges(vartotojas.vaidmuo)
    prisijunges.id = vartotojas.id
    return prisijunges

def registruoti_vartotoja(vardas, pavarde, el_pastas, slapt_hash, vaidmuo):
    vartotojas = Vartotojas(vardas=vardas, pavarde=pavarde, el_pastas=el_pastas, password_hash=slapt_hash, vaidmuo=vaidmuo)
    db.session.add(vartotojas)
    db.session.commit()

def patikrinti_ar_nera(email):
    vartotojas = db.session.execute(db.select(Vartotojas).filter(Vartotojas.el_pastas==email)).scalars().one_or_none()
    return vartotojas is None

def rasti_vartotoja(email, pwd):
    vartotojas = db.session.execute(db.select(Vartotojas).filter(Vartotojas.el_pastas==email)).scalars().one_or_none()
    if vartotojas:
        if patikrinti_slapt_hash(pwd, vartotojas.password_hash):
            return vartotojas
    return None

def gauti_slapt_hash(slaptazodis):
    return pbkdf2_sha256.hash(slaptazodis)

def patikrinti_slapt_hash(slaptazodis, slaptazodis_hash):
    return pbkdf2_sha256.verify(slaptazodis, slaptazodis_hash)

def ar_prisijunges():
    return 