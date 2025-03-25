from app import app
from extensions import db
from models.fakultetas import Fakultetas
from sqlalchemy import select

with app.app_context():
    fakultetai = ["Informatikos fakultetas","Verslo fakultetas","Inžinerijos ir informatikos fakultetas","Kompiuterių mokslų fakultetas"]

    for pavadinimas in fakultetai:
        stmt = select(Fakultetas(pavadinimas == pavadinimas))
        egzistuojantis = db.session.execute(stmt).scalars().first()

        if not egzistuojantis:
            db.session.add(Fakultetas(pavadinimas=pavadinimas))
    db.session.commit()
