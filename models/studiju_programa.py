from extensions import db

class StudijuPrograma(db.Model):
    __tablename__ = 'studiju_programos'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique=True)
    pavadinimas = db.Column(db.String(50), nullable=False)