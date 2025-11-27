
import os
from flask import Flask, render_template, request, redirect, session, flash, url_for  
from controller import *
from werkzeug.utils import secure_filename

# ---- FLASK -----

def route (app):

    @app.route('/')
    @app.route('/login')
    def pag_login():
        param ={}
        cerrarSesion()
        return login(param)
 
    @app.route('/registro')
    def pag_registro():
        param ={}
        cerrarSesion()
        return registro(param)
    
    @app.route('/inicio')
    def pag_inicio():
        return inicio()
    
    
    @app.route('/actividad')
    @app.route('/actividad/<id_hijo>')
    def pag_actividad(id_hijo=None):
        return actividad(id_hijo)
    

    @app.route('/cuenta')
    def pag_cuenta():
        return cuenta()
    
    @app.route('/ingresar')
    def pag_ingresar():
        return ingresar()
    
    @app.route('/iniciopadre')
    def pag_iniciopadre():
        return iniciopadre()
    
    @app.route('/notificaciones')
    def pag_notificaciones():
        return notificaciones()
    
    @app.route('/hijo/<id_hijo>')
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
    @app.route('/transferir/<id_hijo>')
    def pag_transferir(id_hijo=None):
        return transferir(id_hijo)
    

    #get se ve, post no. get manda menos info.
    #archivos y contraseñas con post


    @app.route('/signin', methods =["GET", "POST"])
    def signin(): 
        return validar_login(request)
    
    @app.route('/signup', methods =["GET", "POST"])
    def signup(): 
        return registrarse(request)
    
    @app.route('/modificardatos', methods =["GET", "POST"])
    def modificar(): 
        param={}
        return cambiardatos(param, request)

    @app.route('/logout')
    def logout(): 
        cerrarSesion()
        return redirect('/')
    
    @app.route('/ejecutartransferencia', methods=["GET","POST"])
    def ejecutar_tr(): 
        return ejecutar_transferencia(request)
    

    