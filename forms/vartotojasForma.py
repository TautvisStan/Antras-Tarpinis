from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, DateTimeLocalField, SubmitField, validators, PasswordField, EmailField, RadioField
from wtforms_sqlalchemy import fields

from services.studiju_programa_actions import view_studiju_programa

class VartotojasForma(FlaskForm):
    vardas = StringField("Vardas", [validators.InputRequired()])
    pavarde = StringField("Pavarde", [validators.InputRequired()])
    vaidmuo = RadioField("Vaidmuo", [validators.InputRequired()], choices=["Studentas", "Dėstytojas","Administratorius"])
    el_pastas = StringField("El.paštas", [validators.InputRequired()])
    password = StringField("Slaptažodis", [validators.InputRequired()])
    submit = SubmitField("Sukurti")

