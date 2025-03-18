from extensions import db

class Vartotojas(db.Model):
    __tablename__ = 'vartotojai'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique=True)
    vardas = db.Column(db.String(50), nullable=False)
    pavarde = db.Column(db.String(50), nullable=False)
    el_pastas = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(50), nullable=False)
    vaidmuo = db.Column(db.String(50), nullable=False)
    studiju_programa_id = db.Column(db.Integer, db.ForeignKey('studiju_programos.id'), nullable=True)
    grupe_id = db.Column(db.Integer, db.ForeignKey('grupes.id'), nullable=True)