from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class FakultetasForma(FlaskForm):
    pavadinimas = StringField("Fakulteto pavadinimas", validators=[InputRequired()])
    submit = SubmitField("Sukurti")