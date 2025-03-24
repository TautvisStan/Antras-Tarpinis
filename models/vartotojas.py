from extensions import db
import datetime

class Vartotojas(db.Model):
    __tablename__ = 'vartotojai'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique=True)
    vardas = db.Column(db.String(50), nullable=False)
    pavarde = db.Column(db.String(50), nullable=False)
    el_pastas = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    vaidmuo = db.Column(db.String(50), nullable=False)
    studiju_programa_id = db.Column(db.Integer, db.ForeignKey('studiju_programos.id'), nullable=True)
    grupe_id = db.Column(db.Integer, db.ForeignKey('grupes.id'), nullable=True)
    profilio_pav = db.Column(db.String(50), nullable=True)    #Nuoroda i profilio nuotrauka
    ikelimo_data = db.Column(db.DateTime, nullable=True) # foto ikelimo data
    el_pat = db.Column(db.Boolean, nullable=False, default=False) #El patvirtintas
    el_pat_data = db.Column(db.DateTime, nullable=True)
    dest_pat = db.Column(db.Boolean, nullable=True) #Admin turi patvirtinti dest
    dest_pat_data = db.Column(db.DateTime, nullable=True)
    aktyvumas = db.Column(db.Boolean, default=True)
    nesekmingi_bandymai = db.Column(db.Integer, default = 0)
    blokavimo_laikas = db.Column(db.DateTime, nullable = True)

    # Ryšiai
    studiju_programa = db.relationship('StudijuPrograma', back_populates='studentai', foreign_keys=[studiju_programa_id])
    grupe = db.relationship('Grupe', back_populates='studentai', foreign_keys=[grupe_id])
    moduliai = db.relationship('Modulis', secondary='studentai_moduliai', back_populates='studentai')
    destomi_moduliai = db.relationship('Modulis', back_populates='destytojas', foreign_keys='Modulis.destytojas_id')
    studentai_moduliai = db.relationship('StudentasModulis', back_populates='studentai', foreign_keys='StudentasModulis.studentas_id')
    studento_pasiekimai = db.relationship('StudentoPasiekimai', back_populates='studentas')

    
    def __repr__(self):
        return f"Vartotojas('{self.vardas} {self.pavarde}')"
    
    # Flask-Login reikalavimai
    @property
    def is_active(self):
        return True
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    
    def __repr__(self):
        return f"Vartotojas('{self.vardas} {self.pavarde}')"
    