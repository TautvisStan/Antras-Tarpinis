from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, DateTimeLocalField, SubmitField, validators, TimeField
from wtforms_sqlalchemy import fields
from models.modulis import Modulis
from extensions import db
from sqlalchemy import select

class PaskaitaForma(FlaskForm):
    pavadinimas = StringField("Pavadinimas", [validators.InputRequired()])
    savaites_diena = IntegerField('Savaitės diena', [validators.InputRequired()])
    laikas_nuo = TimeField('Laikas nuo', [validators.InputRequired()])
    laikas_iki = TimeField('Laikas iki', [validators.InputRequired()])

    modulis_id = fields.QuerySelectField('Modulis', query_factory=lambda: db.session.execute(select(Modulis)).scalar().all(), get_label='pavadinimas')
    submit = SubmitField("Patvirtinti")
    




    