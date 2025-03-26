from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, TimeField, SubmitField
from wtforms.validators import InputRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from models.modulis import Modulis
from extensions import db
from sqlalchemy import select

class PaskaitaForma(FlaskForm):
    pavadinimas = StringField("Pavadinimas", validators=[InputRequired()])
    savaites_diena = IntegerField("Savaites diena", validators=[InputRequired()])
    laikas_nuo = TimeField("Laikas nuo", validators=[InputRequired()])
    laikas_iki = TimeField("Laikas iki", validators=[InputRequired()])
   
    """ 
    Originalus kodas: query_factory=lambda: db.session.execute(select(Modulis)).scalar().all() turėjo kelias problemas:
    execute(select(Modulis)) grąžina Result objektą, o .scalar() grąžina tik vieną reikšmę (ne sąrašą), todėl .all() po .scalar() sukeltų klaidą.
    Teisingas būdas: db.session.scalars(select(Modulis)).all() – scalars() grąžina objektų sąrašą (pvz., visus Modulis įrašus), o .all() paverčia tai Python sąrašu.
    Pridėtas allow_blank=True, kad būtų galimybė palikti lauką tuščią (jei tai leidžiama Jusu logikoje; jei ne, galima pašalinti).
"""   
   
    modulis_id = QuerySelectField(
        "Modulis",
        query_factory=lambda: db.session.scalars(select(Modulis)).all(),
        get_label="pavadinimas",
        allow_blank=True
    )
    submit = SubmitField("Patvirtinti")

    