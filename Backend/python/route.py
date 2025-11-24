
import os
from flask import Flask, render_template, request, redirect, session, flash, url_for  
from controller import *
from werkzeug.utils import secure_filename

# ---- FLASK -----

def route (app):

    @app.route('/')
    @app.route('/login')
    def pag_login():

        cerrarSesion()
        param={}
        return login(param)
 
    @app.route('/registro')
    def pag_registro():
        cerrarSesion()
        return registro()
    
    @app.route('/inicio')
    def pag_inicio():
        return inicio()
    
    
    @app.route('/actividad')
    @app.route('/actividad/<int:id_hijo>')
    def pag_actividad(id_hijo=None):
        return actividad(id_hijo)
    

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
    
    @app.route('/hijo/<int:id_hijo>')
    def pag_padre2(id_hijo):
        return padre2(id_hijo)
    
    @app.route('/pendiente')
    def pag_pendiente():
        return pendiente()
    
    @app.route('/quitar')
    def pag_quitar():
        return quitar()
    
    @app.route('/solicitar')
    def pag_solicitar():
        return solicitar()
    
    @app.route('/transferir')
    @app.route('/transferir/<int:id_hijo>')
    def pag_transferir(id_hijo=None):
        return transferir(id_hijo)
    

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
    