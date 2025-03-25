from extensions import db

class StudijuPrograma(db.Model):
    __tablename__ = 'studiju_programos'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    pavadinimas = db.Column(db.String(50), nullable=False)
    specializacija_id = db.Column(db.Integer, db.ForeignKey('specializacijos.id'))


    grupes = db.relationship('Grupe',back_populates='studiju_programa', foreign_keys='Grupe.studiju_programa_id')

    studentai = db.relationship('Vartotojas',back_populates='studiju_programa', foreign_keys='Vartotojas.studiju_programa_id')
    moduliai = db.relationship('Modulis', back_populates='studiju_programa')
    specializacija = db.relationship('Specializacija', back_populates='stud_programos')
    
    def __repr__(self):
        return f'<StudijuPrograma {self.pavadinimas}>'