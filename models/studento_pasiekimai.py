from extensions import db
from datetime import date

class StudentoPasiekimai(db.Model):
    __tablename__ = 'studento_pasiekimai'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    data = db.Column(db.Date, nullable = False)
    studentas_id = db.Column(db.Integer, db.ForeignKey('vartotojai.id'), nullable=False)
    paskaita_id = db.Column(db.Integer, db.ForeignKey('paskaitos.id'), nullable = False)
    pazymys = db.Column(db.Integer, nullable = True)
    nedalyvavo = db.Column(db.Boolean, default=False)

    studentas = db.relationship('Vartotojas', back_populates = 'studento_pasiekimai', foreign_keys=[studentas_id])
    paskaita = db.relationship('Paskaita', back_populates = 'studento_pasiekimai', foreign_keys=[paskaita_id])

