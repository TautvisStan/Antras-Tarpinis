from extensions import db

class Specializacija(db.Model):
    __tablename__ = 'specializacijos'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True)
    pavadinimas = db.Column(db.String(50), nullable=False)
    fakultetas_id = db.Column(db.Integer, db.ForeignKey('fakultetai.id'))


    fakultetas = db.relationship('Fakultetas', back_populates='specializacijos')
    stud_programos = db.relationship('StudijuPrograma', back_populates='specializacija')


    def __repr__(self):
        return f'<Specializacija {self.pavadinimas}>'