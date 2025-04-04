from extensions import db

class Atsiskaitymas(db.Model):
    __tablename__ = 'atsiskaitymai'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pavadinimas = db.Column(db.String(80), nullable=True)
    data_nuo = db.Column(db.DateTime, nullable=True) 
    data_iki = db.Column(db.DateTime, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    aprasymas = db.Column(db.String(500), nullable=True)
    modulis_id = db.Column(db.Integer, db.ForeignKey('moduliai.id'), nullable=True)

    # Ryšiai
    modulis = db.relationship('Modulis',back_populates='atsiskaitymai', foreign_keys=[modulis_id])
    studentai_moduliai = db.relationship('StudentasModulis', back_populates = 'atsiskaitymas')
    testai = db.relationship('Testas', back_populates='atsiskaitymas')

    def __repr__(self):
        return f'Atsiskaitymas: {self.pavadinimas}, {self.id}, {self.aprasymas}, {self.date}'
