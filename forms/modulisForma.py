from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, IntegerField, DateTimeLocalField, SubmitField, TimeField, FieldList, FormField
from wtforms.validators import InputRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from extensions import db
from models.studiju_programa import StudijuPrograma
from sqlalchemy import select
from models.fakultetas import Fakultetas

class PaskaitaForma(FlaskForm):
    pavadinimas = StringField("Paskaitos pavadinimas", [InputRequired()])
    savaites_diena = IntegerField("Savaitės diena (1-7)", [InputRequired()])
    laikas_nuo = TimeField("Laikas nuo", format='%H:%M', validators=[InputRequired()])
    laikas_iki = TimeField("Laikas iki", format='%H:%M', validators=[InputRequired()])

class AtsiskaitymasForma(FlaskForm):
    pavadinimas = StringField(
        "Pavadinimas",
        # choices=[("Egzaminas", "Egzaminas"), ("Labaratorinis", "Labaratorinis"), ("Kursinis", "Kursinis")],
        validators=[InputRequired()]
    )
    date = DateTimeLocalField("Data", format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    # laikas_nuo = DateTimeLocalField("Data nuo", validators=[InputRequired()])
    # laikas_iki = DateTimeLocalField("Data iki", validators=[InputRequired()])
    # aprasymas = StringField("Aprasymas", validators=[InputRequired()])
    submit = SubmitField("Pateikti")

class ModulisForma(FlaskForm):
    pavadinimas = StringField("Pavadinimas", [InputRequired()])
    aprasymas = StringField("Aprašymas", [InputRequired()])
    kreditai = IntegerField("Kreditai", [InputRequired()])
    semestro_informacija = StringField("Semestro informacija", [InputRequired()])
    egzaminas_data = DateTimeLocalField("Egzamino data", format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    studiju_programa = QuerySelectField('Studijų programa', 
                                        query_factory=lambda: db.session.execute(select(StudijuPrograma)).scalars().all(), 
                                        get_label='pavadinimas', 
                                        allow_blank=False, 
                                        validators=[InputRequired()])
    paskaitos = FieldList(FormField(PaskaitaForma), min_entries=1, label="Paskaitos")
    atsiskaitymai = FieldList(FormField(AtsiskaitymasForma), min_entries=0, label="Atsiskaitymai")
    fakultetas = QuerySelectField('Fakultetas', 
                                        query_factory=lambda: db.session.execute(select(Fakultetas)).scalars().all(), 
                                        get_label='pavadinimas', 
                                        allow_blank=False, 
                                        validators=[InputRequired()])

    submit = SubmitField("Sukurti")

    # studiju_programa = fields.QuerySelectField('Studijų programa', query_factory=lambda: db.session.execute(select(StudijuPrograma)).scalar().all(), get_label='pavadinimas')




    