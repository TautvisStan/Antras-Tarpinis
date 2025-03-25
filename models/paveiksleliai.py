from flask import current_app
import os
from werkzeug.utils import secure_filename

class PaveiksleliuValdymas:
    @staticmethod
    def ikelti_paveikslelius(files, vartotojo_id):

        # Įkelia paveikslėlius ir grąžina nuorodų sąrašą.

        nuorodos = []
        for file in files:
            if file and PaveiksleliuValdymas._leidziamas_failo_formatas(file.filename):
                filename = secure_filename(f"{vartotojo_id}_{file.filename}")
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                nuorodos.append(f"/uploads/{filename}")
                
        return nuorodos

    @staticmethod
    def _leidziamas_failo_formatas(filename):
        """
        Patikrina, ar failo formatas yra leidžiamas.
        """
        leidziami_formatai = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in leidziami_formatai 
    
