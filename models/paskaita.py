from datetime import datetime
from extensions import db

class Paskaita(db.Model):
    __tablename__ = 'paskaitos'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique=True)
    pavadinimas = db.Column(db.String(50), nullable=False)
    savaites_diena = db.Column(db.Integer, nullable=False)
    laikas_nuo = db.Column(db.Time, nullable=False)
    laikas_iki = db.Column(db.Time, nullable=False)
    tipas = db.Column(db.String(50), nullable=False) # paskaita, atsiskaitymas, egzaminas 

    modulis_id = db.Column(db.Integer, db.ForeignKey('moduliai.id'), nullable=True)


    modulis = db.relationship('Modulis',back_populates='paskaitos', foreign_keys=[modulis_id])
    studento_pasiekimai = db.relationship('StudentoPasiekimai', back_populates='paskaita')

    def __repr__(self):
        return f'<Paskaita {self.pavadinimas}>'