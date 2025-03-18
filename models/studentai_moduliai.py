from extensions import db

class StudentasModulis(db.Model):
    __tablename__ = 'studentai_moduliai'
    studentas_id = db.Column(db.Integer, db.ForeignKey('vartotojai.id'), primary_key = True, nullable=False)
    modulis_id = db.Column(db.Integer, db.ForeignKey('moduliai.id'), primary_key = True, nullable=False)