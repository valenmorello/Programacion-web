from flask import request, session, redirect, render_template
from datetime import datetime
from model import *
from werkzeug.utils import secure_filename
import os
from uuid import uuid4
from appConfig import config


#--------------------------------------------------------------------------------------------
# diccionario_sesion carga la sesion en un diccionario python y lo retorna


def diccionario_sesion():
    param = {}
    param['id'] = session.get('id_usuario')
    param['usuario'] = session.get('nombre_usuario')
    param['rol'] = session.get('rol')
    param['codfam'] = session.get('codfam')
    param['nombre'] = session.get('nombre')
    param['apellido'] = session.get('apellido')
    param['saldo'] = session.get('saldo')

    return param

#--------------------------------------------------------------------------------------------

def inicio(): #HIJOS
    if haySesion():
        param = diccionario_sesion()
        res = render_template('inicio.html', param=param)
    else:
        res = redirect('/')
    return res
   

def iniciopadre():
    cf = session['codfam']
    param = diccionario_sesion()
    param['hijos'] = encontrar_hijos(param['codfam']) #este elemento del diccionario es un diccionario
    return render_template('iniciopadre.html', param=param)


def padre2(id_hijo):
    if haySesion():
        param = diccionario_sesion()
        param['hijo_dic'] = buscar_por_id(id_hijo)
        res = render_template('padre2.html', param=param, id_hijo=id_hijo) 
    else:
        res = redirect('/')
    return res


def login(param):
    return render_template('index.html', param=param)


def actividad(id_hijo):
    if haySesion():
        param = {}
        param['datos_usuario'] = diccionario_sesion()
        
        if id_hijo == None:
            param['actividad'] = tabla_actividad(param['administrador']['id'])

        else:
            param['hijo'] = buscar_por_id(id_hijo)
            param['actividad'] = tabla_actividad(id_hijo)

        print (param)

        res = render_template('actividad.html', param=param)

    else:
        res = redirect('/')
    return res

  
def transferir(id_hijo):
    if haySesion():
        param = diccionario_sesion()
        if id_hijo != None:
            param['hijo_dic'] = buscar_por_id(id_hijo)
        res = render_template('transferir.html', param=param) 
    else:
        res = redirect('/')
    return res


def cuenta(param):
    if haySesion():
        param = diccionario_sesion()
        res = render_template('cuenta.html', param=param)
    else:
        res = redirect('/')
    return res
    

def ingresar():
    return render_template('ingresar.html')
     

def notificaciones():
    return render_template('notificaciones.html')



def pendiente():
    return render_template('pendiente.html')
    

def quitar():
    return render_template('quitar.html')
    

def registro():
    return render_template('registro.html')
    

def solicitar():
    return render_template('solicitar.html')
    


# ----------------------------------------------------------
def validarusuario(param, request):
    if crearSesion(request):
        if session['rol'] == 1:
            res = iniciopadre()
        elif session['rol'] == 0:
            res = inicio()
    else:
        param['error_login']="Error: Usuario y/o password inválidos"
        res = login(param)
    return res         

# -----------------------------------------------------------

def cambiardatos(param, request):
    if haySesion():
        nombreviejo = session['nombre']  
        apeviejo = session['apellido']
        id = session['id_usuario']

        myrequest={}
        try:         
            getRequest(myrequest)

            if myrequest.get('nombreNuevo') != "" :
                modificarnombre(id, myrequest.get('nombreNuevo'))
                myrequest['nombreNuevo'] = session['nombre']

            if myrequest.get('apellidoNuevo') != "" :
                modificarapellido(id, myrequest.get('apellidoNuevo'))
                myrequest['apellidoNuevo'] = session['apellido']

        except ValueError:                              
            pass
            
    return cuenta(param)


# ---------------------------------------------------------------


def cargarSesion(dicUsuario):
  
    session['id_usuario'] = dicUsuario['id']
    session['nombre']     = dicUsuario['nombre']
    session['apellido']   = dicUsuario['apellido']
    session['codfam']   = dicUsuario['codfam'] 
    session['rol']        = dicUsuario['es_padre']
    session['saldo']   = dicUsuario['saldo']
    session['nombre_usuario']   = dicUsuario['nombre_usuario']
    session['imagen']     = dicUsuario['img']
    session["time"]       = datetime.now()   


def crearSesion(request):
    sesionValida=False
    myrequest={}
    try:         
        getRequest(myrequest)
        dicUsuario={}
        if validar_login(dicUsuario,myrequest.get("usuario"),myrequest.get("contrasenia")):
            cargarSesion(dicUsuario)
            sesionValida = True
    except ValueError:                              
        pass
    return sesionValida

def haySesion():  
    return session.get("nombre_usuario")!=None

def cerrarSesion():
    try:    
        session.clear()
    except:
        pass

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