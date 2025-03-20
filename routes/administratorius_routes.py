from flask import render_template
from extensions import db
import services.administratorius_actions as ad_act
from forms.vartotojasForma import VartotojasForma
from flask import request,flash,url_for,redirect


def init_administratorius_routes(app):
    @app.route('/statistika')
    def atvaizduoti_statistika():
        vartotoju_skaicius,moduliu_skaicius,studiju_programu_skaicius,grupiu_skaicius = ad_act.gauti_statistika()
        
        return render_template('statistika.html', vartotoju_skaicius=vartotoju_skaicius,moduliu_skaicius=moduliu_skaicius,studiju_programu_skaicius=studiju_programu_skaicius,grupiu_skaicius=grupiu_skaicius)
    
    @app.route('/administratorius/vartotojai')
    def vartotojai():

        return render_template ('administratorius_vartotojai.html', vartotojai = ad_act.gauti_vartotojus())
    
    @app.route('/administratorius/vartotojai/perziureti/<id>', methods=['GET', 'POST'])
    def perziureti_vartotoja(id):
        vartotojas = ad_act.gauti_vartotoja(id)
        return render_template('vartotojo_perziura.html',vartotojas=vartotojas)
    
    @app.route('/administratorius/vartotojai/sukurti', methods=['GET', 'POST'])
    def sukurti_nauja_vartotoja():
        
        form = VartotojasForma()
        if request.method == 'GET':
            return render_template('vartotojas_forma.html', form=form)
        else:
            try:
                vardas = form.vardas.data
                pavarde = form.pavarde.data
                vaidmuo = form.vaidmuo.data
               
                ad_act.sukurti_vartotoja(vardas,pavarde,vaidmuo)
                flash("Sekmingai sukurta")
                return redirect(url_for('vartotojai'))
            except Exception:
                pass
            return render_template("vartotojas_forma.html", form=form)  

    @app.route('/administratorius/vartotojai/redaguoti/<id>', methods=['GET', 'POST'])
    def redaguoti_vartotoja(id):
       vartotojas = ad_act.gauti_vartotoja(id)
       form = VartotojasForma(obj = vartotojas)

       if request.method == 'GET':
           return render_template('vartotojas_forma_redaguoti.html', form=form, id=id)
       else:
            try:
                vardas = form.vardas.data
                pavarde = form.pavarde.data
                vaidmuo = form.vaidmuo.data
                ad_act.redaguoti_vartotoja(vartotojas,vardas,pavarde,vaidmuo)
                flash("Sekmingai atnaujinta")
                return redirect(url_for('vartotojai'))
            except Exception as e:
                pass
            return render_template('vartotojas_forma_redaguoti.html', form=form, id=id)   
       
    @app.route('/administratorius/vartotojai/istrinti/<id>', methods=['GET', 'POST'])
    def panaikinti_vartotoja(id):
        ad_act.istrinti_vartotoja(id)
        flash("Sekmingai pasalinta")
        return redirect(url_for('vartotojai'))



           
       



                


