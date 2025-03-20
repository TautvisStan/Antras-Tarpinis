from extensions import db

class Uzduotis(db.Model):
    __tablename__ = 'uzduotys'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique=True)
    pavadinimas = db.Column(db.String(80), nullable=True)
    data_nuo = db.Column(db.DateTime(50), nullable=False)
    data_iki = db.Column(db.DateTime(50), nullable=False)
    aprasymas = db.Column(db.String(50), nullable=False)

    modulis_id = db.Column(db.Integer, db.ForeignKey('moduliai.id'), nullable=True)

    #TODO modulis = db.relationship('Modulis',back_populates='uzduotys', foreign_keys=[modulis_id])