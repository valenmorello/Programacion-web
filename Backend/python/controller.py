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
    param['img'] = session.get('imagen')

    return param

#-------------- Localizacion de paginas y carga de parametros -----------------------------------------

def login(param):
    return render_template('index.html', param=param)


def registro(param):
    return render_template('registro.html', param=param)


def inicio(): #hijos 
    if haySesion():
        param = diccionario_sesion()
        res = render_template('inicio.html', param=param)
    else:
        res = redirect('/')
    return res
   

def iniciopadre(): #padres
    if haySesion():
        param = diccionario_sesion()
        param['hijos'] = encontrar_hijos(param['codfam']) #este elemento del diccionario es un diccionario
        print(param['hijos'])
        res = render_template('iniciopadre.html', param=param)
    else:
        res = redirect('/')
    return res


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


def solicitar(error=None):
    if haySesion():
        param=diccionario_sesion()
        param['mis_solicitudes'] = mis_soicitudes(param['id'])
        param['error'] = error
        res = render_template('solicitar.html', param=param)
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
    

def ingresar(error = None):
    if haySesion():
        param = diccionario_sesion()
        param['error'] = error
        res = render_template('ingresar.html', param=param)
    else:
        res = redirect('/')
    return res
    
     
def notificaciones(error=None):
    if haySesion():
        param = diccionario_sesion()
        param['error'] = error
        param['solicitudes'] = consultar_solicitudes(param['codfam'])
        param['hijos'] = hijos_pendientes(param['codfam'])

        return render_template('notificaciones.html', param=param)
    else:
        return redirect('/')


def pendiente():
    return render_template('pendiente.html')

def quitar(id_hijo, error = None):
    if haySesion():
        param = diccionario_sesion()
        param['id_hijo'] = id_hijo
        param['error'] = error
        res = render_template('quitar.html', param=param)
    else:
        res = redirect('/')
    return res
    
#--------Ingresar Dinero ------------------

def ejecutar_ingreso(request):
    myrequest={}
    getRequest(myrequest)

    id = session['id_usuario']
    monto = int(myrequest['montoIngresar'])
    if monto > 0:
        if ingreso_dinero(id, monto) != None: 
                    session['saldo'] = saldoactual(id)
                    res = ingresar(error="Ingreso Exitoso! ✅")

        else: 
            res = ingresar(error="Hubo un error con el ingreso") #hizo rollback
    else:
        res = ingresar(error="Ingrese un monto")
    return res

#-----Quitar dinero-----------------

def ejecutar_quitado(request, id_hijo):
    myrequest={}
    getRequest(myrequest)

    monto = int(myrequest['montoQuitar'])
    id = session['id_usuario']
    fecha = datetime.now()
    motivo = 'Quitado por administrador ({})'.format(session['nombre']) 

    if monto > 0 and monto <= saldoactual(id_hijo):  
        if carga_transferencia(id_hijo, id, monto, motivo, fecha) != None: 
                    session['saldo'] = saldoactual(id)
                    res = quitar(id_hijo, error="Quitado Exitoso! ✅")

        else: 
            res = quitar(id_hijo, error="Hubo un error con el ingreso") #hizo rollback
    elif monto > 0 and monto > session['saldo']:
        res = quitar(id_hijo, error="El monto es mayor al saldo") 
    else:
        res = quitar(id_hijo, error="Ingrese un monto")
    return res

# ----------------------Transferencias------------------------------------

def ejecutar_transferencia(request):
        
        myrequest={}
        getRequest(myrequest)
        
        id_receptor = find_id(myrequest['usuarioDestino'])

        if id_receptor != []: # [] es que no existe y none si hubo un error con conectDB()

            id = session['id_usuario'] 
            monto = int(myrequest['monto'])
            motivo = myrequest['motivo']
            fecha = datetime.now()

            if saldoactual(id) >= monto:
                if carga_transferencia(id, id_receptor, monto, motivo, fecha) != None: 
                    
                    session['saldo'] = saldoactual(id)
                    res = transferir(error="¡Transferencia Exitosa! ✅")

                else: 
                    res = transferir(error="Hubo un error con la transferencia") #hizo rollback
            else:
                res = transferir(error="SALDO INSUFICIENTE ❌")
        else:
            res = transferir(error="USUARIO INVALIDO")

        return res


#-----------------SOLICITAR-------------

def ejecutar_solicitud(request):
    myrequest = {}
    getRequest(myrequest)

    id_hijo = session['id_usuario']
    monto = int(myrequest.get('montoSolicitar', 0))
    fecha = datetime.now()
    estado = "pendiente"

    if agregar_solicitud(id_hijo, monto, fecha, estado):
        res = solicitar(error="Solicitud exitosa")
    else:
        res = solicitar(error="Hubo un error en la solicitud")
    
    return res

def mostrar_solicitudes():
    if not haySesion():
        return redirect('/')

    codfam = session['codfam']
    lista_solicitudes = consultar_solicitudes(codfam)

    return notificaciones(solicitudes=lista_solicitudes)


#---- MANEJO DE SOLICITUD POR PARTE DEL PADRE ------------

def rechazar(id_solicitud):
    error = None
    if obtener_solicitud(id_solicitud) != None:
        actualizar_estado_solicitud(id_solicitud, 'rechazada')
        error = 'Solicitud rechazada'
    return notificaciones()

def aprobar(id_solicitud):
    error = None
    solicitud = obtener_solicitud(id_solicitud) #obtiene el resto de datos de la solicitud
    if solicitud:
        id_hijo, monto, estado = solicitud
        if estado == 'pendiente':          #para asegruarnos de o resolver 2 veces 
            
            id_padre = session['id_usuario']
            saldo_padre = saldoactual(id_padre)

            if saldo_padre > monto:

                fecha = datetime.now()
                motivo = "Aprobación de solicitud"
                carga_transferencia(id_padre, id_hijo, monto, motivo, fecha)
                actualizar_estado_solicitud(id_solicitud, 'aprobada')
                session['saldo'] = saldoactual(id_padre)

            else:
                error = 'Saldo Insuficiente para resolver la slicitud'
    
    res = notificaciones(error)
    return res
        
    

# ---------------- LOG IN ------------------------------------------

def validar_login(request):
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

# ---------------- REGISTRO ------------------------------------------

def registrarse(request):   # ESTO HABRIA QUE CAMBIARLOCON AYJAX
    myrequest={}
    getRequest(myrequest)    

    res = None
    if not (existe_nombre_usuario(myrequest['usuario'])):  # no se pueden usuaros repe

        if myrequest['select'] == 'padre':
            es_padre = 1
            admitido = 1
            codfam = random.randint(100000, 999999)
            while existe_codfam(codfam):
                codfam = random.randint(100000, 999999)

        elif myrequest['select'] == 'hijo':
            es_padre = 0
            admitido = 0
            codfam = myrequest['codigoFamiliar']

        nombre = myrequest['nombre']
        apellido = myrequest['apellido']
        nombre_usuario = myrequest['usuario']
        contrasenia = myrequest['contrasenia']

        diResult = {}
        upload_file(diResult)
        print(diResult)
        imagen_info = diResult.get('imagen', {})
        
        if imagen_info.get('file_error') is False:
            img = imagen_info.get('file_name_new', '')
        else:
            img = ''

        if registrar_usuario_nuevo(nombre, apellido, codfam, es_padre, contrasenia, nombre_usuario, admitido, img) != None:
            res = validar_registro (nombre_usuario, contrasenia)

        else:
            param = {}
            param['error']="ERROR. intentelo nuevamente" # ESTO HABRIA QUE CAMBIARLOCON AYJAX
            res = registro(param)

    else:
        param = {}
        param['error']="Usuario existente" # ESTO HABRIA QUE CAMBIARLOCON AYJAX
        res = registro(param)

    return res

def validar_registro(nombre_usuario, contrasenia):
    dicUsuario = {}
    validar_usuario(dicUsuario, nombre_usuario, contrasenia)
    cargarSesion(dicUsuario)

    if session['rol'] == 1:
        res = iniciopadre()
    elif session['rol'] == 0:
        res = pendiente()
    return res

# ----------------- Cambiar datos------------------------------------------

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
        if validar_usuario(dicUsuario,myrequest.get("usuario"),myrequest.get("contrasenia")):
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

# ---------------------- Manejo de subida de datos ---------------------------

def upload_file (diResult) :
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif', '.jpeg']
    MAX_CONTENT_LENGTH = 1024 * 1024     
    if request.method == 'POST' :         
        for key in request.files.keys():  
            diResult[key]={} 
            diResult[key]['file_error']=False            

            f = request.files[key] 
            if f.filename!="":     
                #filename_secure = secure_filename(f.filename)
                file_extension=str(os.path.splitext(f.filename)[1])
                filename_unique = uuid4().__str__() + file_extension
                path_filename=os.path.join( config['upload_folder'] , filename_unique)
                # Validaciones
                if file_extension not in UPLOAD_EXTENSIONS:
                    diResult[key]['file_error']=True
                    diResult[key]['file_msg']='Error: No se admite subir archivos con extension '+file_extension
                if os.path.exists(path_filename):
                    diResult[key]['file_error']=True
                    diResult[key]['file_msg']='Error: el archivo ya existe.'
                    diResult[key]['file_name']=f.filename
                try:
                    if not diResult[key]['file_error']:
                        diResult[key]['file_error']=True
                        diResult[key]['file_msg']='Se ha producido un error.'

                        f.save(path_filename)   
                        diResult[key]['file_error']=False
                        diResult[key]['file_name_new']=filename_unique
                        diResult[key]['file_name']=f.filename
                        diResult[key]['file_msg']='OK. Archivo cargado exitosamente'
 
                except:
                        pass
            else:
                diResult[key]={} # viene vacio el input del file upload

    # si existe el archivo devuelve True
    # os.path.exists(os.path.join('G:\\directorio\\....\\uploads',"agua.png"))

    # borrar un archivo
    # os.remove(os.path.join('G:\\directorio\\.....\\uploads',"agua.png"))

# ---------------------------------------------------------------

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