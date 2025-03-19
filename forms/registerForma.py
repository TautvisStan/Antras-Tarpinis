from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, DateTimeLocalField, SubmitField, validators, PasswordField, EmailField, RadioField
from wtforms_sqlalchemy import fields

class RegisterForma(FlaskForm):
    vardas = StringField("Vardas", [validators.InputRequired()])
    pavarde = StringField("Pavarde", [validators.InputRequired()])
    el_pastas = EmailField("El. Paštas", [validators.InputRequired()])
    slaptazodis = PasswordField("Slaptažodis, bent: 1 mažoji, 1 didžioji, 1 skaičius, 8 viso", [validators.InputRequired()])
    vaidmuo = RadioField("Vaidmuo", [validators.InputRequired()], choices=["Studentas", "Dėstytojas"], )
    submit = SubmitField("Prisijungti")