from extensions import db
import datetime

class Rezultatas(db.Model):
    __tablename__ = 'rezultatai'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vartotojas_id = db.Column(db.Integer, db.ForeignKey('vartotojai.id'), nullable=False)
    testas_id = db.Column(db.Integer, db.ForeignKey('testai.id'), nullable=False)
    rezultatas = db.Column(db.Integer, nullable=False)  # Gautas balas
    atlikimo_data = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Ryšiai
    vartotojas = db.relationship('Vartotojas', backref='testu_rezultatai')
    
    def __repr__(self):
        return f'<Rezultatas {self.vartotojas_id} - {self.testas_id}: {self.rezultatas}>'