# from datetime import datetime
# from extensions import db
# from models.vartotojas import Vartotojas
# from models.modulis import Modulis
# from models.grupes import Grupe
# from models.studiju_programa import StudijuPrograma

# def gauti_statistika():
#     vartotoju_skaicius = db.session.execute(db.select(db.func.count()).select_from(Vartotojas)).scalar()
#     moduliu_skaicius = db.session.execute(db.select(db.func.count()).select_from(Modulis)).scalar()
#     studiju_programu_skaicius = db.session.execute(db.select(db.func.count()).select_from(StudijuPrograma)).scalar()
#     grupiu_skaicius = db.session.execute(db.select(db.func.count()).select_from(Grupe)).scalar()

#     vartotoju_skaicius = vartotoju_skaicius if vartotoju_skaicius is not None else 0
#     moduliu_skaicius = moduliu_skaicius if moduliu_skaicius is not None else 0
#     studiju_programu_skaicius = studiju_programu_skaicius if studiju_programu_skaicius is not None else 0
#     grupiu_skaicius = grupiu_skaicius if grupiu_skaicius is not None else 0

#     return vartotoju_skaicius,moduliu_skaicius,studiju_programu_skaicius,grupiu_skaicius 

# def gauti_vartotojus():
#     vartotojai = db.session.execute(db.select(Vartotojas)).scalars().all()
#     return vartotojai

# def sukurti_vartotoja(vardas,pavarde,vaidmuo,el_pastas,password_hash):
#     vartotojas = Vartotojas(vardas=vardas, pavarde=pavarde, vaidmuo=vaidmuo, el_pastas=el_pastas, password_hash=password_hash)
#     db.session.add(vartotojas)
#     db.session.commit()

# def gauti_vartotoja(id):
#     vartotojas = db.session.get(Vartotojas, id)
#     return vartotojas

# def redaguoti_vartotoja(vartotojas,vardas,pavarde,vaidmuo):
#     vartotojas.vardas = vardas
#     vartotojas.pavarde = pavarde
#     vartotojas.vaidmuo = vaidmuo
#     db.session.commit()

# def istrinti_vartotoja(id):
#     vartotojas = db.session.get(Vartotojas, id)
#     db.session.delete(vartotojas)
#     db.session.commit()

# # def istrinti_vartotoja(vartotojas):
# #     try:
# #         db.session.delete(vartotojas)
# #         db.session.commit()  
# #     except Exception as e:
# #         db.session.rollback()  
# #         raise Exception(f"Klaida trinant vartotoją: {e}")
    
# def uzblokuoti_vartotoja(vartotojas):
#     try:
#         vartotojas.aktyvumas = False
#         db.session.commit()  
#     except Exception as e:
#         db.session.rollback()  
#         raise Exception(f"Klaida užblokuojant vartotoją: {e}")

# def patvirtinti_destytoja(id):
#     destytojas = db.session.get(Vartotojas, id)
#     destytojas.dest_pat = True
#     destytojas.dest_pat_data = datetime.now()
#     db.session.commit()

from datetime import datetime
from extensions import db
from models.vartotojas import Vartotojas
from models.modulis import Modulis
from models.grupes import Grupe
from models.studiju_programa import StudijuPrograma

def gauti_statistika():
    """Grąžina pagrindinę sistemos statistiką: vartotojų, modulių, studijų programų ir grupių skaičių"""
    vartotoju_skaicius = db.session.execute(db.select(db.func.count()).select_from(Vartotojas)).scalar()
    moduliu_skaicius = db.session.execute(db.select(db.func.count()).select_from(Modulis)).scalar()
    studiju_programu_skaicius = db.session.execute(db.select(db.func.count()).select_from(StudijuPrograma)).scalar()
    grupiu_skaicius = db.session.execute(db.select(db.func.count()).select_from(Grupe)).scalar()

    vartotoju_skaicius = vartotoju_skaicius if vartotoju_skaicius is not None else 0
    moduliu_skaicius = moduliu_skaicius if moduliu_skaicius is not None else 0
    studiju_programu_skaicius = studiju_programu_skaicius if studiju_programu_skaicius is not None else 0
    grupiu_skaicius = grupiu_skaicius if grupiu_skaicius is not None else 0

    return vartotoju_skaicius, moduliu_skaicius, studiju_programu_skaicius, grupiu_skaicius 

def gauti_vartotojus():
    """Grąžina visų vartotojų sąrašą"""
    vartotojai = db.session.execute(db.select(Vartotojas)).scalars().all()
    return vartotojai

def sukurti_vartotoja(vardas, pavarde, vaidmuo, el_pastas, password_hash, studiju_programa=None, 
                      dest_pat=None, profilio_pav=None, ikelimo_data=None):
    """Sukuria naują vartotoją sistemoje
    
    Args:
        vardas: vartotojo vardas
        pavarde: vartotojo pavardė
        vaidmuo: vartotojo vaidmuo (Studentas, Dėstytojas, Administratorius)
        el_pastas: vartotojo el. pašto adresas
        password_hash: užšifruotas slaptažodis
        studiju_programa: studijų programos ID (jei taikoma)
        dest_pat: dėstytojo patvirtinimo būsena (False - nepatvirtintas, True - patvirtintas, None - netaikoma)
        profilio_pav: profilio paveikslėlio failo pavadinimas (jei yra)
        ikelimo_data: paveikslėlio įkėlimo data
    """
    vartotojas = Vartotojas(
        vardas=vardas, 
        pavarde=pavarde, 
        vaidmuo=vaidmuo, 
        el_pastas=el_pastas, 
        password_hash=password_hash,
        studiju_programa_id=studiju_programa,
        dest_pat=dest_pat,
        profilio_pav=profilio_pav,
        pav_ikelimo_data=ikelimo_data,
        el_pat=True,  # Admin sukurti vartotojai automatiškai patvirtinti
        registration_date=datetime.now(),
        aktyvumas=True
    )
    db.session.add(vartotojas)
    db.session.commit()

def gauti_vartotoja(id):
    """Grąžina vartotoją pagal ID"""
    vartotojas = db.session.get(Vartotojas, id)
    return vartotojas

def redaguoti_vartotoja(vartotojas, vardas, pavarde, vaidmuo, studiju_programa=None):
    """Atnaujina vartotojo duomenis
    
    Args:
        vartotojas: Vartotojo objektas
        vardas: naujas vartotojo vardas
        pavarde: nauja vartotojo pavardė
        vaidmuo: naujas vartotojo vaidmuo
        studiju_programa: nauja studijų programa (ID)
    """
    vartotojas.vardas = vardas
    vartotojas.pavarde = pavarde
    vartotojas.vaidmuo = vaidmuo
    vartotojas.studiju_programa_id = studiju_programa
    db.session.commit()

def istrinti_vartotoja(id):
    """Ištrina vartotoją iš duomenų bazės pagal ID"""
    vartotojas = db.session.get(Vartotojas, id)
    if vartotojas:
        db.session.delete(vartotojas)
        db.session.commit()
    else:
        raise ValueError(f"Vartotojas su ID {id} nerastas")
    
def uzblokuoti_vartotoja(vartotojas):
    """Užblokuoja vartotoją (pakeičia aktyvumo būseną į False)"""
    try:
        vartotojas.aktyvumas = False
        db.session.commit()  
    except Exception as e:
        db.session.rollback()  
        raise Exception(f"Klaida užblokuojant vartotoją: {e}")

def patvirtinti_destytoja(id):
    """Patvirtina dėstytoją (nustato dest_pat į True)"""
    destytojas = db.session.get(Vartotojas, id)
    if destytojas and destytojas.vaidmuo == "Dėstytojas":
        destytojas.dest_pat = True
        destytojas.dest_pat_data = datetime.now()
        db.session.commit()
    else:
        raise ValueError(f"Dėstytojas su ID {id} nerastas arba vartotojas nėra dėstytojas")

# Modulių valdymo funkcijos
def gauti_modulius():
    """Grąžina visus modulius"""
    moduliai = db.session.execute(db.select(Modulis)).scalars().all()
    return moduliai

def sukurti_moduli(pavadinimas, aprasas, kreditai):
    """Sukuria naują modulį"""
    modulis = Modulis(pavadinimas=pavadinimas, aprasas=aprasas, kreditai=kreditai)
    db.session.add(modulis)
    db.session.commit()
    return modulis

# Studijų programų valdymo funkcijos
def gauti_studiju_programas():
    """Grąžina visas studijų programas"""
    programos = db.session.execute(db.select(StudijuPrograma)).scalars().all()
    return programos

def sukurti_studiju_programa(pavadinimas, aprasas):
    """Sukuria naują studijų programą"""
    programa = StudijuPrograma(pavadinimas=pavadinimas, aprasas=aprasas)
    db.session.add(programa)
    db.session.commit()
    return programa

# Grupių valdymo funkcijos
def gauti_grupes():
    """Grąžina visas grupes"""
    grupes = db.session.execute(db.select(Grupe)).scalars().all()
    return grupes

def sukurti_grupe(pavadinimas, studiju_programa_id, metai):
    """Sukuria naują grupę"""
    grupe = Grupe(pavadinimas=pavadinimas, studiju_programa_id=studiju_programa_id, metai=metai)
    db.session.add(grupe)
    db.session.commit()
    return grupe