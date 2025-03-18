from flask import request, jsonify
from extensions import db, app
from models.vartotojas import Vartotojas
from models.paveiksleliai import PaveiksleliuValdymas

@app.route('/vartotojas/<int:id>/ikelti_paveikslelius', methods=['POST'])
def ikelti_paveikslelius(id):
    vartotojas = Vartotojas.query.get_or_404(id)
    files = request.files.getlist('paveiksleliai')
    if files:
        nuorodos = PaveiksleliuValdymas.ikelti_paveikslelius(files, id)
        if nuorodos:
            vartotojas.paveiksleliai = nuorodos
            db.session.commit()
            return jsonify({"message": "Paveikslėliai sėkmingai įkelti", "nuorodos": nuorodos}), 200
    return jsonify({"message": "Nepavyko įkelti paveikslėlių"}), 400

