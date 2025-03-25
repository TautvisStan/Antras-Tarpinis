from extensions import db

class Fakultetas(db.Model):
    __tablename__ = 'fakultetai'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True)
    pavadinimas = db.Column(db.String(100), nullable=False)

    studentai = db.relationship('Vartotojas', back_populates='fakultetas')
    moduliai = db.relationship('Modulis', back_populates='fakultetas')

    def __repr__(self):
        return f'<Fakultetas {self.pavadinimas}>'


