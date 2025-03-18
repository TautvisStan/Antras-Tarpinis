from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, DateTimeLocalField, SubmitField, validators
from wtforms_sqlalchemy import fields
class ModulisForma(FlaskForm):
    pavadinimas = StringField("Pavadinimas", [validators.InputRequired()])
    aprasymas = StringField("Aprasymas", [validators.InputRequired()])
    kreditai = IntegerField("Kreditai")
    semestro_informacija = StringField("Semestro informacija", [validators.InputRequired()])
    submit = SubmitField("Sukurti")


    #   pavadinimas = db.Column(db.String(50), nullable=False)
    # aprasymas = db.Column(db.String(50), nullable=False)
    # kreditai = db.Column(db.Integer, nullable=False)
    # semestro_informacija = db.Column(db.String(50), nullable=False)
    # departamentas = fields.QuerySelectField("Departamentas", query_factory=lambda: db.session.execute(select(Departamentas)).scalars().all(), get_label='pavadinimas')