from extensions import db

class Grupe(db.Model):
    __tablename__ = 'grupes'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique=True)
    pavadinimas = db.Column(db.String(50), nullable=False)
    studiju_programa_id = db.Column(db.Integer, db.ForeignKey('studiju_programos.id'), nullable=True)