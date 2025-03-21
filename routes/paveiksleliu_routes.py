from flask import request, flash, redirect, url_for, render_template
from models.vartotojas import Vartotojas, db

from services import issaugoti_paveiksleli

from datetime import datetime
from forms import registerForma

def inicijuoti_marsrutus(app):
  
       
 

    @app.route('/perziureti_paveiksleli/<int:vartotojo_id>')
    def perziureti_paveiksleli(vartotojo_id):
        vartotojas = Vartotojas.query.get_or_404(vartotojo_id)
        return render_template('profile.html', vartotojas=vartotojas)