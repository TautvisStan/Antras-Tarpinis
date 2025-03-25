from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, DateTimeLocalField, SubmitField, validators
from wtforms_sqlalchemy import fields
from wtforms_sqlalchemy.fields import QuerySelectField
from sqlalchemy import select
from extensions import db
from models.specializacija import Specializacija


class StudijuProgramaForma(FlaskForm):
    pavadinimas = StringField("Pavadinimas", [validators.InputRequired()])
    specializacija = QuerySelectField("Specializacija",
        query_factory=lambda: db.session.execute(select(Specializacija)).scalars().all(),
        get_label="pavadinimas",
        validators=[validators.InputRequired()])

    submit = SubmitField("Sukurti")