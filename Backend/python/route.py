
import os
from flask import Flask, render_template, request, redirect, session, flash, url_for  
from controller import *
from werkzeug.utils import secure_filename

# ---- FLASK -----

def route (app):

    # ----- RUTAS A PAGINAS ------

    @app.route('/')
    @app.route('/login')
    def pag_login():
        cerrarSesion()
        param ={}
        param['error_login'] = request.args.get('error')
        return login(param)
 
    @app.route('/registro')
    def pag_registro():
        cerrarSesion()
        param ={}
        param['error'] = request.args.get('error')
        return registro(param)
    
    @app.route('/inicio')
    def pag_inicio():
        return inicio()
    
    @app.route('/iniciopadre')
    def pag_iniciopadre():
        return iniciopadre()
    
    @app.route('/actividad')
    @app.route('/actividad/<id_hijo>')
    def pag_actividad(id_hijo=None):
        return actividad(id_hijo)
    
    @app.route('/cuenta')
    def pag_cuenta():
        return cuenta()
    
    
    
    @app.route('/notificaciones')
    def pag_notificaciones():
        status = request.args.get('status')
        return notificaciones(status)
    

    @app.route('/hijo/<int:id_hijo>')
    def pag_padre2(id_hijo):
        return padre2(id_hijo)           


    @app.route('/pendiente')
    def pag_pendiente():
        param = {}
        return pendiente(param)           

    @app.route('/ingresar')
    def pag_ingresar():
        status = request.args.get('status')
        return ingresar(status)
    
    @app.route('/quitar/<int:id_hijo>')
    def pag_quitar(id_hijo):
        status = request.args.get('status')
        return quitar(id_hijo, status)           


    @app.route('/solicitar')
    def pag_solicitar():
        status = request.args.get('status')
        return solicitar(status) # la ruta del boton se lama /ejecutarsolicitud y la pase para abajo
                     

    @app.route('/transferir')
    @app.route('/transferir/<id_hijo>')
    def pag_transferir(id_hijo=None):
        status = request.args.get('status')
        return transferir(status, id_hijo)
    

    @app.route('/logout')
    def logout(): 
        cerrarSesion()
        return redirect('/')


    # ----- RUTAS DE ENVIO DE INFORMACION -----


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

    
    @app.route('/ejecutartransferencia', methods=["GET","POST"])
    def ejecutar_tr(): 
        return ejecutar_transferencia(request)
    

    @app.route('/ejecutarsolicitud', methods=['GET','POST'])
    def eje_solicitar():
        return ejecutar_solicitud(request)  


    @app.route('/ingreso', methods=["GET","POST"])
    def ejecutar_ing(): 
        return ejecutar_ingreso(request)
    

    @app.route('/quitado/<id_hijo>', methods=["GET","POST"])
    def ejecutar_quit(id_hijo):
        return ejecutar_quitado(request, id_hijo)
    

    @app.route('/aceptar_hijo/<int:id_hijo>')
    def aceptar_hijo_controller(id_hijo):
        aceptar_hijo(id_hijo)
        return redirect('/notificaciones')


    @app.route('/rechazar_hijo/<int:id_hijo>')
    def rechazar_hijo_controller(id_hijo):
        rechazar_hijo(id_hijo)
        return redirect('/notificaciones')
    

    @app.route('/aprobar/<int:id_solicitud>')
    def aprobar_solicitud(id_solicitud):
        return aprobar(id_solicitud)     

    @app.route('/rechazar/<int:id_solicitud>')
    def rechazar_solicitud(id_solicitud):
        return rechazar(id_solicitud)
    
    @app.route('/validar')
    def validar_admision():
        return admision()