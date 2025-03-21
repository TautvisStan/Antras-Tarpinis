import os
from werkzeug.utils import secure_filename
from flask import current_app
from datetime import datetime

def leistinas_failas(failo_pavadinimas):
    return '.' in failo_pavadinimas and \
           failo_pavadinimas.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def issaugoti_profilio_paveiksleli(failas, email):
    if failas and leistinas_failas(failas.filename):
        # Gauname failo pratesima
        pratesimas = failas.filename.rsplit('.', 1)[1].lower()
        # Generuojame unikalu pavadinima: vardas_pavarde_data
        data_str = datetime.now().strftime('%Y%m%d%H%M%S')
        failo_pavadinimas = secure_filename(f"{email}_{data_str}.{pratesimas}")
        
        ikelimo_katalogas = current_app.config['UPLOAD_FOLDER']
        failo_kelias = os.path.join(ikelimo_katalogas, failo_pavadinimas)
        
        os.makedirs(ikelimo_katalogas, exist_ok=True)
        
        failas.save(failo_kelias)
        
        if os.path.exists(failo_kelias):
            return failo_pavadinimas
        else:
            raise Exception("Nepavyko issaugoti failo diske")
    return None