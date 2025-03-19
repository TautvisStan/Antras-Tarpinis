from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, DateTimeLocalField, SubmitField, validators, PasswordField, EmailField
from wtforms_sqlalchemy import fields

class LoginForma(FlaskForm):
    el_pastas = EmailField("El. Paštas", [validators.InputRequired()])
    slaptazodis = PasswordField("Slaptažodis", [validators.InputRequired()])
    submit = SubmitField("Prisijungti")