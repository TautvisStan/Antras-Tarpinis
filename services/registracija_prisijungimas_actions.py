from datetime import datetime
import flask_login
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
    
def prijungti_vartotoja(vartotojas):
    prisijunges = Prisijunges(vartotojas.vaidmuo, vartotojas.studiju_programa_id)
    prisijunges.id = vartotojas.id
    return prisijunges

def registruoti_vartotoja(vardas, pavarde, el_pastas, slapt_hash, vaidmuo, studiju_programa, dest_pat):
    vartotojas = Vartotojas(vardas=vardas, pavarde=pavarde, el_pastas=el_pastas, password_hash=slapt_hash, vaidmuo=vaidmuo, studiju_programa_id=studiju_programa, dest_pat=dest_pat)
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

def gauti_vartotoja_email(email):
    return db.session.execute(db.select(Vartotojas).filter(Vartotojas.el_pastas==email)).scalars().one_or_none()

def patvirtinti_vartotojo_mail(vartotojas):
    vartotojas.el_pat = True
    vartotojas.el_pat_data = datetime.now()
    db.session.commit()

def gauti_slapt_hash(slaptazodis):
    return pbkdf2_sha256.hash(slaptazodis)

def patikrinti_slapt_hash(slaptazodis, slaptazodis_hash):
    return pbkdf2_sha256.verify(slaptazodis, slaptazodis_hash)

def ar_prisijunges():
    return flask_login.current_user.is_authenticated

def gauti_prisijungusio_vaidmeni():
    if ar_prisijunges():
        return flask_login.current_user.vaidmuo
    return "Neprisijungęs"

def patikrinti_roles(roles : list[str]):
    return flask_login.current_user.vaidmuo in roles
        