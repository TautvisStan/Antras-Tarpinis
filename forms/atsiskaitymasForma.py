from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeLocalField, SubmitField, validators
from wtforms_sqlalchemy import fields
from models.modulis import Modulis
from extensions import db
from sqlalchemy import select

class AtsiskaitymasForma(FlaskForm):
    data = DateTimeLocalField('Data', [validators.InputRequired()])
    aprasymas = StringField('Aprašymas'[validators.InputRequired()])
    
    modulis = fields.QuerySelectField('Modulis', query_factory=lambda: db.session.execute(select(Modulis)).scalar().all())
    submit = SubmitField("Pateikti")
    
    
    




    