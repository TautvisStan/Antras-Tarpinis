from flask import redirect, render_template, request, url_for
import flask_login
from extensions import login_manager
import services.registracija_prisijungimas_actions as reg_pr
from services.prisijunges_actions import Prisijunges
def init_login_routes(app):

    @app.route('/401')
    @login_manager.unauthorized_handler
    def neprisijunges():
        return render_template('401.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return '''
                <form action='login' method='POST'>
                    <input type='text' name='email' id='email' placeholder='email'/>
                    <input type='password' name='password' id='password' placeholder='password'/>
                    <input type='submit' name='submit'/>
                </form>
                '''

        email = request.form['email']
        password = request.form['password']
        vartotojas = reg_pr.rasti_vartotoja(email, password) #TODO
        if vartotojas:
            prisijunges = Prisijunges()
            prisijunges.id = vartotojas.id
            flask_login.login_user(prisijunges)
            return redirect(url_for('protected'))

        return 'Bad login'


    @app.route('/protected')
    @flask_login.login_required
    def protected():
        return 'Logged in as: ' + str(flask_login.current_user.id)


    @app.route('/logout')
    @flask_login.login_required
    def logout():
        flask_login.logout_user()
        return 'Logged out'