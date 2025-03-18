from extensions import db

class Atsiskaitymas(db.Model):
    __tablename__ = 'atsiskaitymai'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique=True)
    data = db.Column(db.DateTime(50), nullable=False)
    aprasymas = db.Column(db.String(50), nullable=False)

    modulis_id = db.Column(db.Integer, db.ForeignKey('moduliai.id'), nullable=True)