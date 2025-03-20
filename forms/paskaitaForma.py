from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, DateTimeLocalField, SubmitField, validators, TimeField, RadioField
from wtforms_sqlalchemy import fields
from wtforms.validators import DataRequired
from models.modulis import Modulis
from extensions import db
from sqlalchemy import select

class PaskaitaForma(FlaskForm):
    pavadinimas = StringField("Pavadinimas", [validators.InputRequired()])
    savaites_diena = IntegerField('Savaitės diena', [validators.InputRequired()])
    laikas_nuo = TimeField('Laikas nuo', [validators.InputRequired()])
    laikas_iki = TimeField('Laikas iki', [validators.InputRequired()])
    tipas = RadioField('Tipas', [validators.InputRequired()], choices=["Paskaita", "Atsiskaitymas", "Egzaminas"])
    modulis_id = fields.QuerySelectField('Modulis', query_factory=lambda: db.session.execute(select(Modulis)).scalar().all(), get_label='pavadinimas')
    submit = SubmitField("Patvirtinti"), ("Prideti")
    




    