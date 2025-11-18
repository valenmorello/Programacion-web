from flask import request, session, redirect, render_template
from datetime import datetime
from model import *
from werkzeug.utils import secure_filename
import os
from uuid import uuid4
from appConfig import config


#--------------------------------------------------------------------------------------------

def inicio():
    return render_template('inicio.html')
   

def login(param):
    return render_template('index.html', param=param)
 

def actividad():
    return render_template('actividad.html')
    

def cuenta():
    return render_template('cuenta.html')
    

def ingresar():
    return render_template('ingresar.html')
    

def iniciopadre():
    return render_template('iniciopadre.html')
    

def notificaciones():
    return render_template('notificaciones.html')

def padre2():
    return render_template('padre2.html')
    

def pendiente():
    return render_template('pendiente.html')
    

def quitar():
    return render_template('quitar.html')
    

def registro():
    return render_template('registro.html')
    

def solicitar():
    return render_template('solicitar.html')
    

def transferir():
    return render_template('transferir.html')

# -------------------------------------------------------------------------------------------

#Esta funcion carga el request hecho en el navegador 
# y lo convierte en un diccionario 

def getRequest(diResult):
    if request.method=='POST':
        for name in request.form.to_dict().keys():
            li=request.form.getlist(name)
            if len(li)>1:
                diResult[name]=request.form.getlist(name)
            elif len(li)==1:
                diResult[name]=li[0]
            else:
                diResult[name]=""
    elif request.method=='GET':  
        for name in request.args.to_dict().keys():
            li=request.args.getlist(name)
            if len(li)>1:
                diResult[name]=request.args.getlist(name)
            elif len(li)==1:
                diResult[name]=li[0]
            else:
                diResult[name]=""

# ----------------------------------------------------------
def validarusuario(param, request):
    if crearSesion(request):
        res = inicio()
    else:
        param['error_login']="Error: Usuario y/o password inválidos"
        res = login(param)
    return res         

# -----------------------------------------------------------

def cargarSesion(dicUsuario):
    
    session['id_usuario'] = dicUsuario['id']
    session['nombre']     = dicUsuario['nombre']
    session['apellido']   = dicUsuario['apellido']
    session['cod_fam']   = dicUsuario['codfam'] 
    session['rol']        = dicUsuario['es_padre']
    session['saldo']   = dicUsuario['saldo']
    session['username']   = dicUsuario['nombre_usuario']
    session['imagen']     = dicUsuario['img']
    session["time"]       = datetime.now()   


def crearSesion(request):
    sesionValida=False
    dic_request={}
    try:         
        getRequest(dic_request)
        dicUsuario={}
        if validar_login(dicUsuario,dic_request.get("usuario"),dic_request.get("contrasenia")):
            cargarSesion(dicUsuario)
            sesionValida = True
    except ValueError:                              
        pass
    return sesionValida

def haySesion():  
    '''info:
        Determina si hay una sesion activa observando si en el dict
        session se encuentra la clave 'username'
        retorna True si hay sesión y False si no la hay.
    '''
    return session.get("username")!=None

def cerrarSesion():
    '''info:
        Borra el contenido del dict 'session'
    '''
    try:    
        session.clear()
    except:
        pass