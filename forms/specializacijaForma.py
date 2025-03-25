from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class SpecializacijaForma(FlaskForm):
    pavadinimas = StringField("Specializacija", validators=[InputRequired()])
    submit = SubmitField("Sukurti")