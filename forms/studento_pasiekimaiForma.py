from flask_wtf import FlaskForm
from wtforms import IntegerField, BooleanField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, NumberRange, Optional
from models.vartotojas import Vartotojas
from models.paskaita import Paskaita
from extensions import db
from sqlalchemy import select

class StudentoPasiekimaiForma(FlaskForm):
    studentas = QuerySelectField("Studentas", 
                                 query_factory=lambda: db.session.execute(select(Vartotojas)).scalars().all(), 
                                 get_label="vardas",
                                 validators=[InputRequired()])
    
    paskaita = QuerySelectField("Paskaita", 
                                query_factory=lambda: db.session.execute(select(Paskaita)).scalars().all(), 
                                get_label="pavadinimas",
                                validators=[InputRequired()])  
    
    pazymys = IntegerField("Pažymys (0–10)", 
                           validators=[Optional(), NumberRange(min=0, max=10)])
    nedalyvavo = BooleanField("Nedalyvavo paskaitoje")
    
    submit = SubmitField("Patvirtinti")