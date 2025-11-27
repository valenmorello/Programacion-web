from flask import request, session, redirect, render_template
from datetime import datetime
from model import *
from werkzeug.utils import secure_filename
import os
from uuid import uuid4
from appConfig import config


#--------------------------------------------------------------------------------------------
# Carga los datos dela sesion en un diccionario

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

#-------------- Localizacion de paginas y carga de parametros -----------------------------------------

def login():
    param={}
    return render_template('index.html', param=param)


def registro():
    return render_template('registro.html')


def inicio(): #hijos
    if haySesion():
        param = diccionario_sesion()
        res = render_template('inicio.html', param=param)
    else:
        res = redirect('/')
    return res
   

def iniciopadre(): #padres
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


def actividad(id_hijo):
    if haySesion():
        param = {}
        param = diccionario_sesion()
        
        if id_hijo == None:  # cargamos los datos propios del usuario
            param['actividad'] = tabla_actividad(param['id']) #pasa su propio id

        else:
            param['hijo_dic'] = buscar_por_id(id_hijo)
            param['actividad'] = tabla_actividad(id_hijo)

        res = render_template('actividad.html', param=param)

    else:
        res = redirect('/')
    return res

  
def transferir(id_hijo=None, error=None):
    if haySesion():
        param = diccionario_sesion()
        param['error'] = error
        if id_hijo != None:
            param['hijo_dic'] = buscar_por_id(id_hijo)
        res = render_template('transferir.html', param=param) 
    else:
        res = redirect('/')
    return res


def cuenta():
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
    

def solicitar():
    return render_template('solicitar.html')
    
# ----------------------Transferencias------------------------------------

def ejecutar_transferencia(request):
        
        myrequest={}
        getRequest(myrequest)
        
        id_receptor = find_id(myrequest['usuarioDestino'])

        if id_receptor != [] and id_receptor != None: # [] es que no existe y none si hubo un error con conectDB()
            
            id_receptor = id_receptor[0][0]

            id = session['id_usuario'] 
            saldo = saldoactual(id)

            monto = int(myrequest['monto'])
            motivo = myrequest['motivo']
            fecha = datetime.now()


            if saldo >= monto:
                if carga_transferencia(id, id_receptor, monto, motivo, fecha) != None: 
                    
                    session['saldo'] = saldoactual(id)
                    res = transferir(error="¡Transferencia Exitosa!")

                else: 
                    res = transferir(error="Hubo un error con la transferencia") #hizo rollback
            else:
                res = transferir(error="SALDO INSUFICIENTE")
        else:
            res = transferir(error="USUARIO INVALIDO")

        return res

# ----------------------------------------------------------

def validarusuario(request):
    if crearSesion(request):
        if session['rol'] == 1:
            res = iniciopadre()
        elif session['rol'] == 0:
            res = inicio()
    else:
        param={}
        param['error_login']="Error: Usuario y/o password inválidos"
        res = login(param)
    return res         

# -----------------------------------------------------------

def cambiardatos(param, request):
    if haySesion():

        id = session['id_usuario']
        myrequest={}
        getRequest(myrequest)

        if myrequest.get('nombreNuevo') != "" :
            modificarnombre(id, myrequest.get('nombreNuevo'))
            myrequest['nombreNuevo'] = session['nombre']

        if myrequest.get('apellidoNuevo') != "" :
            modificarapellido(id, myrequest.get('apellidoNuevo'))
            myrequest['apellidoNuevo'] = session['apellido']

    return cuenta()

# ---------------------------------------------------------------
# Funciones de sesion

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