from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, DateTimeLocalField, SubmitField, validators, PasswordField, EmailField
from wtforms_sqlalchemy import fields

class LoginForma(FlaskForm):
    el_pastas = EmailField("El. Paštas", [validators.InputRequired()])
    slaptazodis = PasswordField("Slaptažodis, bent: 1 mažoji, 1 didžioji, 1 skaičius, 8 viso", [validators.InputRequired()])
    submit = SubmitField("Prisijungti")