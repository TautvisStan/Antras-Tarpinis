from extensions import db

class Modulis(db.Model):
    __tablename__ = 'moduliai'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique=True)
    pavadinimas = db.Column(db.String(50), nullable=False)
    aprasymas = db.Column(db.String(50), nullable=False)
    kreditai = db.Column(db.Integer, nullable=False)
    semestro_informacija = db.Column(db.String(50), nullable=False)
    egzaminas_data = db.Column(db.DateTime(50), nullable=False) #prideta egzamino data, kuri tures rysi su tvarkarasciu

    studiju_programa_id = db.Column(db.Integer, db.ForeignKey('studiju_programos.id'), nullable=True)
    destytojas_id = db.Column(db.Integer, db.ForeignKey('vartotojai.id'), nullable=True)
    


    atsiskaitymai = db.relationship('Atsiskaitymas',back_populates='modulis', foreign_keys='Atsiskaitymas.modulis_id')
    #TODO tvarkarasciai = db.relationship('Tvarkarastis',back_populates='moduliai', foreign_keys='Tvarkarastis.atsiskaitymas_id') # tvarkaraštis


    paskaitos = db.relationship('Paskaita',back_populates='modulis', foreign_keys='Paskaita.modulis_id')
    studentai_moduliai = db.relationship('StudentasModulis', back_populates = 'modulis')

  