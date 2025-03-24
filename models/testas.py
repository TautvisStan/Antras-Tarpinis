from extensions import db

class Testas(db.Model):
    __tablename__ = 'testai'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pavadinimas = db.Column(db.String(100), nullable=False)
    modulis_id = db.Column(db.Integer, db.ForeignKey('moduliai.id'), nullable=False)
    atsiskaitymas_id = db.Column(db.Integer, db.ForeignKey('atsiskaitymai.id'), nullable=True)  # Ryšys su atsiskaitymu
    testo_sukurejas = db.Column(db.Integer, db.ForeignKey('vartotojai.id'), nullable=False)
    maksimalus_balas = db.Column(db.Integer, nullable=False, default=100)  # Maksimalus galimas balas

    # Ryšiai
    modulis = db.relationship('Modulis', back_populates='testai')
    atsiskaitymas = db.relationship('Atsiskaitymas', back_populates='testai')
    sukurejas = db.relationship('Vartotojas', backref='sukurti_testai')
    klausimai = db.relationship('Uzduotis', backref='testas', lazy=True)
    rezultatai = db.relationship('Rezultatas', backref='testas', lazy=True)

    def __repr__(self):
        return f'<Testas {self.pavadinimas}>'