from extensions import db

class Uzduotis(db.Model):
    __tablename__ = 'uzduotys'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    tekstas = db.Column(db.String(500), nullable=False)
    testas_id = db.Column(db.Integer, db.ForeignKey('testai.id'), nullable=False)
    atsakymas = db.Column(db.String(200), nullable=False)  # Teisingas atsakymas

    def __repr__(self):
        return f'<Uzduotis {self.id} iš testo {self.testas_id}>'