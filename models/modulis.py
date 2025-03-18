from extensions import db

class Modulis(db.Model):
    __tablename__ = 'moduliai'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique=True)
    pavadinimas = db.Column(db.String(50), nullable=False)
    aprasymas = db.Column(db.String(50), nullable=False)
    kreditai = db.Column(db.Integer, nullable=False)
    semestro_informacija = db.Column(db.String(50), nullable=False)
    #studiju tvarkarastis
    studiju_programa_id = db.Column(db.Integer, db.ForeignKey('studiju_programos.id'), nullable=True)
    destytojas_id = db.Column(db.Integer, db.ForeignKey('vartotojai.id'), nullable=True)