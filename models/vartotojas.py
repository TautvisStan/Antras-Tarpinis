from extensions import db

class Vartotojas(db.Model):
    __tablename__ = 'vartotojai'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique=True)
    vardas = db.Column(db.String(50), nullable=False)
    pavarde = db.Column(db.String(50), nullable=False)
    el_pastas = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    vaidmuo = db.Column(db.String(50), nullable=False)
    studiju_programa_id = db.Column(db.Integer, db.ForeignKey('studiju_programos.id'), nullable=True)
    grupe_id = db.Column(db.Integer, db.ForeignKey('grupes.id'), nullable=True)
    profilio_pav = db.Column(db.String(50), nullable=True)    #Nuoroda i profilio nuotrauka
    el_pat = db.Column(db.Boolean, nullable=False, default=False) #El patvirtintas
    el_pat_data = db.Column(db.DateTime, nullable=True)
    dest_pat = db.Column(db.Boolean, nullable=True) #Admin turi patvirtinti dest
    dest_pat_data = db.Column(db.DateTime, nullable=True)
    aktyvumas = db.Column(db.Boolean, default=True)

    studiju_programa = db.relationship('StudijuPrograma',back_populates='studentai', foreign_keys=[studiju_programa_id])

    grupe = db.relationship('Grupe',back_populates='studentai', foreign_keys=[grupe_id])
    studentai_moduliai = db.relationship('StudentasModulis', back_populates = 'studentas')
    