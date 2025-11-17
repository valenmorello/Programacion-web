
from flask import render_template

# ---- FLASK -----

def route (app):

    @app.route('/inicio')
    def inicio():
        return render_template('inicio.html')
    
    @app.route('/actividad')
    def actividad():
        return render_template('actividad.html')
    
    @app.route('/cuenta')
    def cuenta():
        return render_template('cuenta.html')
    
    @app.route('/ingresar')
    def ingresar():
        return render_template('ingresar.html')
    
    @app.route('/iniciopadre')
    def iniciopadre():
        return render_template('iniciopadre.html')
    
    @app.route('/notificaciones')
    def notificaciones():
        return render_template('notificaciones.html')
    
    @app.route('/padre2')
    def padre2():
        return render_template('padre2.html')
    
    @app.route('/pendiente')
    def pendiente():
        return render_template('pendiente.html')
    
    @app.route('/quitar')
    def quitar():
        return render_template('quitar.html')
    
    @app.route('/registro')
    def registro():
        return render_template('registro.html')
    
    @app.route('/solicitar')
    def solicitar():
        return render_template('solicitar.html')
    
    @app.route('/transferir')
    def transferir():
        return render_template('transferir.html')
    

    