from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeLocalField, SubmitField, TimeField, FieldList, FormField
from wtforms.validators import InputRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from extensions import db
from models.studiju_programa import StudijuPrograma
from sqlalchemy import select

class PaskaitaForma(FlaskForm):
    pavadinimas = StringField("Paskaitos pavadinimas", [InputRequired()])
    savaites_diena = IntegerField("Savaitės diena (1-7)", [InputRequired()])
    laikas_nuo = TimeField("Laikas nuo", format='%H:%M', validators=[InputRequired()])
    laikas_iki = TimeField("Laikas iki", format='%H:%M', validators=[InputRequired()])

class AtsiskaitymasForma(FlaskForm):
    pavadinimas = StringField("Atsiskaitymo pavadinimas", [InputRequired()])
    data = DateTimeLocalField("Data", format='%Y-%m-%dT%H:%M', validators=[InputRequired()])

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
    submit = SubmitField("Sukurti")

    # studiju_programa = fields.QuerySelectField('Studijų programa', query_factory=lambda: db.session.execute(select(StudijuPrograma)).scalar().all(), get_label='pavadinimas')




    