from extensions import db

# studentu_moduliai = db.Table('studentu_moduliai',
#     db.Column('vartotojas_id', db.Integer, db.ForeignKey('vartotojai.id'), primary_key=True),
#     db.Column('modulis_id', db.Integer, db.ForeignKey('moduliai.id'), primary_key=True)
# )

class Modulis(db.Model):
    __tablename__ = 'moduliai'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique=True)
    pavadinimas = db.Column(db.String(50), nullable=False)
    aprasymas = db.Column(db.String(50), nullable=False)
    kreditai = db.Column(db.Integer, nullable=False)
    semestro_informacija = db.Column(db.String(50), nullable=False)
    egzaminas_data = db.Column(db.DateTime(50), nullable=False) 

    studiju_programa_id = db.Column(db.Integer, db.ForeignKey('studiju_programos.id'), nullable=True)
    destytojas_id = db.Column(db.Integer, db.ForeignKey('vartotojai.id'), nullable=True)
    fakultetas_id = db.Column(db.Integer, db.ForeignKey('fakultetai.id'))
    
    # Ryšiai
    studiju_programa = db.relationship('StudijuPrograma', back_populates='moduliai')
    destytojas = db.relationship('Vartotojas', back_populates='destomi_moduliai', foreign_keys=[destytojas_id])
    paskaitos = db.relationship('Paskaita', back_populates='modulis', foreign_keys='Paskaita.modulis_id')
    atsiskaitymai = db.relationship('Atsiskaitymas', back_populates='modulis', foreign_keys='Atsiskaitymas.modulis_id')
    studentai = db.relationship('Vartotojas', secondary="studentai_moduliai", back_populates='moduliai')
    studentai_moduliai = db.relationship('StudentasModulis', back_populates='moduliai')
    fakultetas = db.relationship('Fakultetas',back_populates='moduliai')

    testai = db.relationship('Testas', back_populates='modulis', foreign_keys='Testas.modulis_id')


    def __repr__(self):
        return f'<Modulis {self.pavadinimas}>'

  