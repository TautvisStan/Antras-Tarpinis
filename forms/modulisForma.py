from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, DateTimeLocalField, SubmitField, validators
from wtforms_sqlalchemy import fields
from models.studiju_programa import StudijuPrograma
from extensions import db
from sqlalchemy import select

class ModulisForma(FlaskForm):
    pavadinimas = StringField("Pavadinimas", [validators.InputRequired()])
    aprasymas = StringField("Aprasymas", [validators.InputRequired()])
    kreditai = IntegerField("Kreditai")
    semestro_informacija = StringField("Semestro informacija", [validators.InputRequired()])
    submit = SubmitField("Sukurti")

    studiju_programa = fields.QuerySelectField('Studijų programa', query_factory=lambda: db.session.execute(select(StudijuPrograma)).scalar().all(), get_label='pavadinimas')




    