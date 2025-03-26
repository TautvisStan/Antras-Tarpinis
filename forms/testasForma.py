from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired
from forms.atsiskaitymasForma import AtsiskaitymasForma  # Jei reikia pasirinkti atsiskaitymą

class KlausimasForma(FlaskForm):
    tekstas = StringField('Klausimo tekstas', validators=[DataRequired()])
    atsakymas = StringField('Teisingas atsakymas', validators=[DataRequired()])

class TestasForma(FlaskForm):
    pavadinimas = StringField('Testo pavadinimas', validators=[DataRequired()])
    maksimalus_balas = IntegerField('Maksimalus balas', validators=[DataRequired()], default=100)
    atsiskaitymas = FormField(AtsiskaitymasForma, default=None)  # Pasirenkamas atsiskaitymas
    klausimai = FieldList(FormField(KlausimasForma), min_entries=1, max_entries=20)
    submit = SubmitField('Sukurti testą')