from flask_wtf import FlaskForm
from wtforms import RadioField, DateTimeLocalField, SubmitField, StringField
from wtforms.validators import InputRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from models.modulis import Modulis
from extensions import db
from sqlalchemy import select

class AtsiskaitymasForma(FlaskForm):
    data = DateTimeLocalField('Data', validators=[InputRequired()])
    aprasymas = StringField('Aprašymas', validators=[InputRequired()])
    
    modulis = QuerySelectField('Modulis', query_factory=lambda: db.session.execute(select(Modulis)).scalar().all())
    submit = SubmitField("Pateikti")
    
    
    

# Integravau su moduliu atsiskaitymas
class AtsiskaitymasForma(FlaskForm):
    pavadinimas = RadioField(
        "Pavadinimas",
        choices=[("Egzaminas", "Egzaminas"), ("Labaratorinis", "Labaratorinis"), ("Kursinis", "Kursinis")],
        validators=[InputRequired()]
    )
    data_nuo = DateTimeLocalField("Data nuo", validators=[InputRequired()])
    data_iki = DateTimeLocalField("Data iki", validators=[InputRequired()])
    aprasymas = StringField("Aprasymas", validators=[InputRequired()])
    modulis = QuerySelectField(
        "Modulis",
        query_factory=lambda: db.session.scalars(select(Modulis)).all(),
        get_label="pavadinimas",
        allow_blank=True
    )
    submit = SubmitField("Pateikti")



    