from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms_sqlalchemy import fields
from models.modulis import Modulis
from extensions import db
from sqlalchemy import select

class GrupesForma(FlaskForm):
    pavadinimas = StringField("Pavadinimas", [validators.InputRequired()])
    submit = SubmitField("Patvirtinti")



    