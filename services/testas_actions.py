from extensions import db
from sqlalchemy import select
from models.testas import Testas
from models.uzduotis import Uzduotis
from models.rezultatas import Rezultatas
from models.studentai_moduliai import StudentasModulis
from flask_login import current_user

def sukurti_testa(pavadinimas, modulis_id, atsiskaitymas_id, klausimai_data, maksimalus_balas):
    #  Sukuria naują testą su klausimais
    try:
        if current_user.vaidmuo != 'destytojas':
            raise Exception("Tik dėstytojai gali kurti testus")
        
        testas = Testas(
            pavadinimas=pavadinimas,
            modulis_id=modulis_id,
            atsiskaitymas_id=atsiskaitymas_id,
            testo_sukurejas=current_user.id,
            maksimalus_balas=maksimalus_balas
        )
        db.session.add(testas)
        db.session.flush()  # Gauti testo ID prieš pridedant klausimus

        for klausimas in klausimai_data:
            uzduotis = Uzduotis(
                tekstas=klausimas['tekstas'],
                testas_id=testas.id,
                atsakymas=klausimas['atsakymas']
            )
            db.session.add(uzduotis)
        
        db.session.commit()
        return testas
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Testo sukūrimo klaida: {str(e)}")

def gauti_testa(testo_id):
    #  Grąžina testą pagal ID
    try:
        testas = db.session.execute(select(Testas).where(Testas.id == testo_id)).scalars().first()
        if not testas:
            raise Exception(f"Testas su ID {testo_id} nerastas")
        return testas
    except Exception as e:
        raise Exception(f"Klaida gaunant testą: {str(e)}")

def pateikti_testo_atsakymus(testo_id, atsakymai):
    #  Studentas pateikia atsakymus, gauna rezultatą ir atnaujina modulio pažymį
    try:
        if current_user.vaidmuo != 'studentas':
            raise Exception("Tik studentai gali spręsti testus")
        
        # Patikriname, ar studentas jau sprendė šį testą
        esamas_rezultatas = db.session.execute(
            select(Rezultatas).where(
                Rezultatas.vartotojas_id == current_user.id,
                Rezultatas.testas_id == testo_id
            )
        ).scalars().first()
        if esamas_rezultatas:
            raise Exception("Šį testą jau išsprendėte")

        testas = gauti_testa(testo_id)
        klausimai = testas.klausimai
        balai = 0
        balas_uz_klausima = testas.maksimalus_balas / len(klausimai) if klausimai else 0

        # Apskaičiuojame balus pagal pateiktus atsakymus
        for klausimas in klausimai:
            pateiktas_ats = atsakymai.get(str(klausimas.id), "").strip()
            if pateiktas_ats == klausimas.atsakymas.strip():
                balai += balas_uz_klausima

        # Įrašome rezultatą
        rezultatas = Rezultatas(
            vartotojas_id=current_user.id,
            testas_id=testo_id,
            rezultatas=int(balai)
        )
        db.session.add(rezultatas)

        # Atnaujiname StudentasModulis pažymį
        studentas_modulis = db.session.execute(
            select(StudentasModulis).where(
                StudentasModulis.studentas_id == current_user.id,
                StudentasModulis.modulis_id == testas.modulis_id
            )
        ).scalars().first()

        if not studentas_modulis:
            # Jei įrašas neegzistuoja, sukuriame naują
            studentas_modulis = StudentasModulis(
                studentas_id=current_user.id,
                modulis_id=testas.modulis_id,
                atsiskaitymas_id=testas.atsiskaitymas_id,
                pazymys=balai
            )
            db.session.add(studentas_modulis)
        else:
            # Jei įrašas egzistuoja, atnaujiname pažymį (pvz., pridedame prie esamo)
            studentas_modulis.pazymys = (studentas_modulis.pazymys or 0) + balai
            studentas_modulis.atsiskaitymas_id = testas.atsiskaitymas_id  # Jei atsiskaitymas susietas

        db.session.commit()
        return rezultatas
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Testo pateikimo klaida: {str(e)}")

def atnaujinti_modulio_pazymi(studentas_id, modulis_id):
    #  Apskaičiuoja vidurkį iš visų testų rezultatų moduliui
    try:
        rezultatai = db.session.execute(
            select(Rezultatas).join(Testas).where(
                Rezultatas.vartotojas_id == studentas_id,
                Testas.modulis_id == modulis_id
            )
        ).scalars().all()

        if rezultatai:
            vidurkis = sum(rez.rezultatas for rez in rezultatai) / len(rezultatai)
            studentas_modulis = db.session.execute(
                select(StudentasModulis).where(
                    StudentasModulis.studentas_id == studentas_id,
                    StudentasModulis.modulis_id == modulis_id
                )
            ).scalars().first()
            if studentas_modulis:
                studentas_modulis.pazymys = vidurkis
            else:
                studentas_modulis = StudentasModulis(
                    studentas_id=studentas_id,
                    modulis_id=modulis_id,
                    pazymys=vidurkis
                )
                db.session.add(studentas_modulis)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Pažymio atnaujinimo klaida: {str(e)}")