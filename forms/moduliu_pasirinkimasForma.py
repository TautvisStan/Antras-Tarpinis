from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms_sqlalchemy import fields
from models.modulis import Modulis
from extensions import db
from sqlalchemy import select

class ModuliuPasirinkimoForma(FlaskForm):
    moduliai = fields.QuerySelectField('Pasirinkite modulius', query_factory=lambda: db.session.execute(select(Modulis)).scalar().all(), get_label='pavadinimas')
    submit = SubmitField("Patvirtinti")



    