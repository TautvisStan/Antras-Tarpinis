from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, DateTimeLocalField, SubmitField, validators
from wtforms_sqlalchemy import fields
from wtforms_sqlalchemy.fields import QuerySelectField
from sqlalchemy import select
from extensions import db



class StudijuProgramaForma(FlaskForm):
    pavadinimas = StringField("Pavadinimas", [validators.InputRequired()])
    submit = SubmitField("Sukurti")