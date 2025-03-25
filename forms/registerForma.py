from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SelectField, StringField, IntegerField, DateTimeLocalField, SubmitField, validators, PasswordField, EmailField, RadioField
from wtforms_sqlalchemy import fields
from extensions import db
from models.fakultetas import Fakultetas
from wtforms_sqlalchemy.fields import QuerySelectField
from sqlalchemy import select

from services.studiju_programa_actions import view_studiju_programa

class RegisterForma(FlaskForm):
    vardas = StringField("Vardas", [validators.InputRequired()])
    pavarde = StringField("Pavarde", [validators.InputRequired()])
    el_pastas = EmailField("El. Paštas", [validators.InputRequired()])
    slaptazodis = PasswordField("Slaptažodis", [validators.InputRequired()])
    vaidmuo = RadioField("Vaidmuo", [validators.InputRequired()], choices=["Studentas", "Dėstytojas"])
    profilio_pav = FileField("Profilio Paveikslelis",
    validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Leidžiami tik paveikslėliai (jpg, png, gif)!')])
    studiju_programa = fields.QuerySelectField("Studiju Programa", query_factory=lambda: view_studiju_programa(), get_label='pavadinimas')

    fakultetas = QuerySelectField('Fakultetas', 
                                        query_factory=lambda: db.session.execute(select(Fakultetas)).scalars().all(), 
                                        get_label='pavadinimas')

    submit = SubmitField("Prisijungti")

    