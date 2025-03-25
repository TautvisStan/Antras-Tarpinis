from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, DateTimeLocalField, SubmitField, validators, PasswordField, EmailField, RadioField
from wtforms_sqlalchemy import fields
from models.studiju_programa import StudijuPrograma
from models.fakultetas import Fakultetas
from sqlalchemy import select
from wtforms_sqlalchemy.fields import QuerySelectField
from extensions import db


from services.studiju_programa_actions import view_studiju_programa

class VartotojasForma(FlaskForm):
    vardas = StringField("Vardas", [validators.InputRequired()])
    pavarde = StringField("Pavarde", [validators.InputRequired()])
    vaidmuo = RadioField("Vaidmuo", [validators.InputRequired()], choices=["Studentas", "Dėstytojas","Administratorius"])
    studiju_programa = QuerySelectField("Studijų programa",
        query_factory=lambda: db.session.execute(select(StudijuPrograma)).scalars().all(),
        get_label="pavadinimas",
        allow_blank=True)

    fakultetas = QuerySelectField("Fakultetas",
        query_factory=lambda: db.session.execute(select(Fakultetas)).scalars().all(),
        get_label="pavadinimas",
        allow_blank=True)
    
    el_pastas = StringField("El.paštas", [validators.InputRequired()])
    password = StringField("Slaptažodis", [validators.InputRequired()])
    submit = SubmitField("Sukurti")

