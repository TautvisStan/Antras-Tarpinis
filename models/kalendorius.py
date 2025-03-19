from extensions import db

class Kalendorius(db.Model):
    __tablename__ = 'kalendorius'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False, unique=True)  # Šventinė/išeiginė diena
    aprasas = db.Column(db.String(100), nullable=True)      # Šventės aprašas