from extensions import db

class Atsiskaitymas(db.Model):
    __tablename__ = 'atsiskaitymai'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique=True)
    data = db.Column(db.DateTime, nullable=False)
    aprasymas = db.Column(db.String(50), nullable=False)

    modulis_id = db.Column(db.Integer, db.ForeignKey('moduliai.id'), nullable=True)


    modulis = db.relationship('Modulis',back_populates='atsiskaitymai', foreign_keys=[modulis_id])
    studentai_moduliai = db.relationship('StudentasModulis', back_populates = 'atsiskaitymas')


    def __repr__(self):
        return f'Atsiskaitymas {self.id}, {self.aprasymas}, {self.data}'