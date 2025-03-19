from flask import flash, render_template, request, url_for

def init_index_routes(app):
    @app.route('/index')
    def index():
        return render_template("index.html")