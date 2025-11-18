
import os
from flask import Flask, render_template, request, redirect, session, flash, url_for  
from controller import *
from werkzeug.utils import secure_filename

# ---- FLASK -----

def route (app):

    @app.route('/')
    @app.route('/login')
    def pag_login():
        param={}
        return login(param)
 
    @app.route('/registro')
    def pag_registro():
        return registro()
    
    @app.route('/inicio')
    def pag_inicio():
        return inicio()
    
    @app.route('/actividad')
    def pag_actividad():
        return actividad()
    
    @app.route('/cuenta')
    def pag_cuenta():
        param ={}
        return cuenta(param)
    
    @app.route('/ingresar')
    def pag_ingresar():
        return ingresar()
    
    @app.route('/iniciopadre')
    def pag_iniciopadre():
        return iniciopadre()
    
    @app.route('/notificaciones')
    def pag_notificaciones():
        return notificaciones()
    
    @app.route('/padre2')
    def pag_padre2():
        return padre2()
    
    @app.route('/pendiente')
    def pag_pendiente():
        return pendiente()
    
    @app.route('/quitar')
    def pag_quitar():
        return quitar()
    
    @app.route('/solicitar')
    def pag_solicitar():
        return render_template('solicitar.html')
    
    @app.route('/transferir')
    def pag_transferir():
        return render_template('transferir.html')
    

    #get se ve, post no. get manda menos info.
    #archivos y contraseñas con post

    # ESTO NO ANDA Y NO SE PORQUE

    @app.route('/signin', methods =["GET", "POST"])
    def signin(): 
        param={}
        return validarusuario(param, request)
    
    @app.route('/modificardatos', methods =["GET", "POST"])
    def modificar(): 
        param={}
        return cambiardatos(param, request)

    @app.route('/logout')
    def logout(): 
        cerrarSesion()
        return redirect('/')
    