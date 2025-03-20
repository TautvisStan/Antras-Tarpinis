from extensions import db

class Tvarkarastis(db.Model):
    __tablename__ = 'tvarkarasciai'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique=True)
    savaites_diena = db.Column(db.Integer, nullable=False)
    pakaitos_pavadinimas = db.Column(db.String(50), nullable=False)
    laikas_nuo = db.Column(db.Time, nullable=False)
    laikas_iki = db.Column(db.Time, nullable=False)
    
    uzduotis_id = db.Column(db.Time, db.ForeignKey('uzduotys.id'), nullable=True)
    atsiskaitymas_id = db.Column(db.Time, db.ForeignKey('atsiskaitymai.id'), nullable=True)
    modulis_id = db.Column(db.Integer, db.ForeignKey('moduliai.id'), nullable=True)


    modulis = db.relationship('Modulis',back_populates='tvarkarasciai', foreign_keys=[modulis_id])
    atsiskaitymas = db.relationship('Atsiskaitymas', back_populates='tvarkarasciai', foreign_keys=[atsiskaitymas_id])
    uzduotis = db.relationship('Uzduotis', back_populates='tvarkarasciai', foreign_keys=[uzduotis_id])
    
    