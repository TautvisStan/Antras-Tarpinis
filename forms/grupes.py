from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, DateTimeLocalField, SubmitField, validators
from wtforms_sqlalchemy import fields
class GrupesForma(FlaskForm):
    pavadinimas = StringField("Pavadinimas", [validators.InputRequired()])
    submit = SubmitField("Sukurti")