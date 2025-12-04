from flask import request, session, redirect, render_template, url_for
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
            param['actividad'] = tabla_actividad(param['id'], param['usuario']) #pasa su propio id

        else:
            param['hijo_dic'] = buscar_por_id(id_hijo)
            param['actividad'] = tabla_actividad(id_hijo, param['hijo_dic']['nombre_usuario'])

        res = render_template('actividad.html', param=param)

    else:
        res = redirect('/')
    return res

  

def transferir(status, id_hijo=None):
    if haySesion():
        param = diccionario_sesion()

        if status != None:
            param['mostrar_popup'] = True
            param['status'] = status

        if id_hijo != None:
            param['hijo_dic'] = buscar_por_id(id_hijo)

        res = render_template('transferir.html', param=param) 
    else:
        res = redirect('/')
    return res

def solicitar(status):
    if haySesion():
        param=diccionario_sesion()
        param['mis_solicitudes'] = mis_solicitudes(param['id'])

        if status != None:
            param['status'] = status
            param['mostrar_popup'] = True

        res = render_template('solicitar.html', param=param)
    else:
        res = redirect('/')
    return res

def ingresar(status):
    if haySesion():
        param = diccionario_sesion()

        if status != None:
            param['status'] = status
            param['mostrar_popup'] = True
      
        res = render_template('ingresar.html', param=param)
    else:
        res = redirect('/')
    return res  

def quitar(id_hijo, status):
    if haySesion():
        param = diccionario_sesion()
        param['id_hijo'] = id_hijo

        if status != None:
            param['mostrar_popup'] = True
            param['status'] = status
            
        
        res = render_template('quitar.html', param=param)
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
        
def notificaciones(status):
    if haySesion():
        param = diccionario_sesion()
        param['status'] = status
        param['solicitudes'] = consultar_solicitudes(param['codfam'])
        param['hijos'] = hijos_pendientes(param['codfam'])

        return render_template('notificaciones.html', param=param)
    else:
        return redirect('/')

def pendiente(param):
    return render_template('pendiente.html', param=param)

    
#--------Ingresar Dinero ------------------

def ejecutar_ingreso(request):
    myrequest={}
    getRequest(myrequest)

    id = session['id_usuario']
    monto = int(myrequest['montoIngresar'])
    
    if ingreso_dinero(id, monto) != None: 
        session['saldo'] = saldoactual(id)
        res = redirect('/ingresar?status=Ingreso Exitoso!')

    else: 
        res = redirect('/ingresar?status=ERROR CON EL INGRESO')
    
    return res

#-----Quitar dinero-----------------

def ejecutar_quitado(request, id_hijo):
    myrequest={}
    getRequest(myrequest)

    monto = int(myrequest['montoQuitar'])
    id = session['id_usuario']
    fecha = datetime.now()
    motivo = 'Quitado por administrador ({})'.format(session['nombre']) 

    if monto <= saldoactual(id_hijo):  
        if carga_transferencia(id_hijo, id, monto, motivo, fecha) != None: 
                    session['saldo'] = saldoactual(id)
                    res = redirect(url_for('pag_quitar', id_hijo=id_hijo, status='QUITE EXITOSO'))
        else: 
            res = redirect(url_for('pag_quitar', id_hijo=id_hijo, status='ERROR CON EL QUITE'))
    else:
        res = redirect(url_for('pag_quitar', id_hijo=id_hijo, status='SALDO MENOR AL MONTO A QUITAR'))
    
    return res

# ----------------------Transferencia------------------------------------

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
                    res = redirect('/transferir?status=Transferencia exitosa')

                else: 
                    res = redirect('/transferir?status=Error con la transferencia')
            else:
                res = redirect('/transferir?status=SALDO INSUFICIENTE')
        else:
            res = redirect('/transferir?status=USUARIO INVALIDO')

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
        res = redirect('/solicitar?status=Solicitud enviada')
    else:
        res = redirect('/solicitar?status=Error en la solicitud')
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
        actualizar_estado_solicitud(id_solicitud, "rechazado")
    return redirect('/notificaciones?status=Solicitud rechazada')

def aprobar(id_solicitud):
    res = None
    solicitud = obtener_solicitud(id_solicitud) #obtiene el resto de datos de la solicitud
    if solicitud:
        id_hijo, monto, estado = solicitud
        if estado == "pendiente":          #para asegruarnos de o resolver 2 veces 
            
            id_padre = session['id_usuario']
            saldo_padre = saldoactual(id_padre)

            if saldo_padre > monto:

                fecha = datetime.now()
                motivo = "Aprobación de solicitud"
                if carga_transferencia(id_padre, id_hijo, monto, motivo, fecha) != None:
                    actualizar_estado_solicitud(id_solicitud, "aceptado")
                    session['saldo'] = saldoactual(id_padre)
                    res = redirect('/notificaciones?status=Solicitud aprobada')
            else:
                res = redirect('/notificaciones?status=Saldo Insuficiente para resolver la slicitud')
    
    return res
        
# ---------------- LOG IN ------------------------------------------

def validar_login(request):
    if crearSesion(request):
        if session['rol'] == 1:
            res = redirect('/iniciopadre')
        elif session['rol'] == 0:
            res = redirect('/inicio')
    else:
        res = redirect('/login?error=USUARIO Y/O PASSWORD INVALIDOS')
        
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
            res = redirect('/registro?error=ERROR DESCONOCIDO')
    else:
        res = redirect('/registro?error=USUARIO EXISTENTE')

    return res

def validar_registro(nombre_usuario, contrasenia):
    dicUsuario = {}
    validar_usuario(dicUsuario, nombre_usuario, contrasenia)
    cargarSesion(dicUsuario)

    if session['rol'] == 1:
        res = redirect('/iniciopadre')
    elif session['rol'] == 0:
        res = redirect('/pendiente')
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

    return redirect('/cuenta')


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


def admision():
    param = {}
    if verificar_admision(session['id_usuario']) == 1:
        return inicio() 
    else:
        param['admitido'] = 0
        return render_template('pendiente.html', param=param) 
    

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