from mysql_db import *
import random

def buscar_por_id(id):
    sQuery="SELECT * FROM usuarios WHERE id=%s"
    val = (id,)
    mydb = conectarDB(BASE)
    fila = consultarDB(mydb,sQuery,val) #lista de tuplas
    cerrarDB(mydb)

    dic = {}
    if fila!=[]:
        dic['id']=fila[0][0]
        dic['nombre']=fila[0][1]
        dic['apellido']=fila[0][2]
        dic['saldo']= fila[0][5]
        dic['nombre_usuario']=fila[0][7]
        dic['img']=fila[0][9]

    return dic
 
# ------ VALIDAR LOGIIIINNNNNN ---------------

def validar_usuario (dic, username, password):
    res=False
    sQuery="""
    SELECT * FROM  usuarios WHERE  nombre_usuario=%s and contrasenia=%s;"""
    val=(username,password)

    mydb = conectarDB(BASE)
    fila = consultarDB(mydb,sQuery,val)
    cerrarDB(mydb)
    
    if fila!=[]:
        res=True
        dic['id']=fila[0][0]
        dic['nombre']=fila[0][1]
        dic['apellido']=fila[0][2]
        dic['codfam']=fila[0][3] 
        dic['es_padre']=fila[0][4]
        dic['saldo']= fila[0][5]
        dic['contrasenia']=fila[0][6]
        dic['nombre_usuario']=fila[0][7]
        dic['admitido']=fila[0][8]
        dic['img']=fila[0][9]

    return res    

# --------- REGISTROOOO -------------------

def existe_codfam (codfam):
    sQuery="""
        SELECT codigo_Familiar FROM usuarios WHERE codigo_Familiar = %s """
    val = (codfam,)
    mydb = conectarDB(BASE)
    res = consultarDB(mydb,sQuery,val)
    cerrarDB(mydb)
    
    if res == [] or res == None:
        res = False
    else:
        res = True

    return res

def existe_nombre_usuario (nombre_usuario):
    sQuery="""
        SELECT nombre_usuario FROM usuarios WHERE nombre_usuario = %s """
    val = (nombre_usuario,)
    mydb = conectarDB(BASE)
    res = consultarDB(mydb,sQuery,val)
    cerrarDB(mydb)

    if res == [] or res == None:
        res = False
    else:
        res = True
    return res

def registrar_usuario_nuevo(nombre, apellido, codfam, es_padre, contrasenia, nombre_usuario, admitido, img):

    sQuery="""
        INSERT INTO usuarios
        (id, nombres, apellido, codigo_Familiar, es_padre, saldo, contrasenia, nombre_usuario, admitido, img)
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    val = ('Null', nombre, apellido, codfam, es_padre, 0, contrasenia, nombre_usuario, admitido, img,)
    mydb = conectarDB(BASE)
    res = ejecutarDB(mydb, sQuery,val)
    cerrarDB(mydb)  

    return res

#--------  MODIFICAR DATOS ----------------------------

def modificarnombre(id, nuevonombre):
    sQuery="UPDATE usuarios SET nombres=%s WHERE id=%s"
    val = (nuevonombre, id)
    mydb=conectarDB(BASE)
    res = ejecutarDB(mydb,sQuery,val)      
    cerrarDB(mydb)
    return res

def modificarapellido(id, nuevoape):
    sQuery="UPDATE usuarios SET apellido=%s WHERE id=%s"
    val = (nuevoape, id)
    mydb=conectarDB(BASE)
    res=ejecutarDB(mydb,sQuery,val)   
    cerrarDB(mydb)
    return res

# ---- PLATA ---------------------------------------

''' (aclaracion de feli) Esta funcion esta hecha diferente a las otras.  
    Como estamos haciendo una transaccion, si hay un error en algun momento con la base de datos
    necesito que haga rollback de los 3 comandos (update, update e insert), porque no puede sumarse
    la plata a uno y que no se le reste al otro. Para eso necesito varios execute con
    un solo commit. Por eso no me sirve usar ejecutarBD()
    
    mydb.start_transaction() --> “A partir de este momento, todas las consultas que hagas
    van a estar agrupadas en una sola operación atómica, hasta que hagas un commit() o un rollback().”
    '''

def carga_transferencia(id_emisor, id_receptor, monto, motivo, fecha):
    
    mydb=conectarDB(BASE)

    res = None
    try:
        mycursor = mydb.cursor()
        mydb.start_transaction()

        mycursor.execute(
            "UPDATE usuarios SET saldo = saldo - %s WHERE id=%s",
            (monto, id_emisor)
        )
        mycursor.execute(
            "UPDATE usuarios SET saldo = saldo + %s WHERE id=%s",
            (monto, id_receptor)
        )
        mycursor.execute("""
            INSERT INTO actividades
            (id, emisor, receptor, motivo, fecha, monto)
            VALUES (%s,%s,%s,%s,%s,%s)""",
            ('Null', id_emisor, id_receptor, motivo, fecha, monto))
 

        mydb.commit()
        res = mycursor.lastrowid

    except mysql.connector.Error as e:
        mydb.rollback()
        print("ERROR ->",e) 

    finally:   
        cerrarDB(mydb)

    return res #retorna las filas afectadas

def saldoactual(id):
    sQuery="SELECT saldo FROM usuarios WHERE id=%s"
    val = (id,)
    mydb = conectarDB(BASE)
    res = consultarDB(mydb,sQuery,val)
    cerrarDB(mydb)

    if res != None:
        res = res[0][0] #para saarlo de la lsta de tuplas

    return res

def find_id (nombre_usuario,):
    sQuery="SELECT id FROM usuarios WHERE nombre_usuario=%s AND admitido=1"
    val = (nombre_usuario,)
    mydb = conectarDB(BASE)
    res = consultarDB(mydb,sQuery,val)
    cerrarDB(mydb)

    if res != [] and res != None:
        res = res[0][0]   #para saarlo de la lsta de tuplas
        
    return res


def ingreso_dinero(id, monto):
    sQuery = "UPDATE usuarios set saldo = saldo + %s where id = %s"
    val = (monto, id)
    mydb=conectarDB(BASE)
    res = ejecutarDB(mydb,sQuery,val)      
    cerrarDB(mydb)
    return res


#--------------- ACTIVIDAAAAAADDDDD-----------------------------

def tabla_actividad(id, nombre_usuario):
    sQuery="""
    SELECT emi.nombre_usuario, emi.nombres, recep.nombre_usuario, recep.nombres,
    act.monto, act.motivo, act.fecha   
    FROM actividades AS act
    INNER JOIN usuarios AS emi ON act.emisor = emi.id
    INNER JOIN usuarios AS recep ON act.receptor = recep.id
    WHERE act.emisor=%s OR act.receptor=%s 
    ORDER BY fecha DESC
    """
    val = (id,id)
    mydb = conectarDB(BASE)
    lista = consultarDB(mydb,sQuery,val) #lista de tuplas
    cerrarDB(mydb)

    print(lista)

    # desglose de lista, armado de tabla
    # [(usuario_emisor, nombre_emisor, usuario_receptor, nombre_receptor, monto, motivo, fecha)]
    transacciones = []
    if lista != [] and lista != None:
        for tupla in lista:
            dic = {}
            if tupla[0] == nombre_usuario: # si el usuario es emisor
                dic['usuario'] = tupla[2]
                dic['nombre'] = tupla[3]    
                dic['monto'] = int(tupla[4])*(-1)

            elif tupla[2] == nombre_usuario: # si el usuario es receptor
                dic['usuario'] = tupla[0]
                dic['nombre'] = tupla[1] 
                dic['monto'] = int(tupla[4])
        
            dic['motivo'] = tupla[5]
            dic['fecha'] = tupla[6]

            transacciones.append(dic)

    return transacciones 


# ------ HIJOOOOOOSSSSSSS -----------------------------------------------------------

# devuelve una lista de tuplas, cada elemento de la lista es un hijo. 

def encontrar_hijos(codfam):
    sQuery="SELECT id, nombres, img FROM usuarios WHERE codigo_Familiar=%s and es_padre=0 and admitido=1"
    val = (codfam,)
    mydb = conectarDB(BASE)
    lista = consultarDB(mydb,sQuery,val) #lista de tuplas
    cerrarDB(mydb)

    #transformarlo en un diccionario para que sea mas facil
    # evito algunos datos porque no me sirven
    diccionario_hijos= {}
    for hijo in lista: #creo un diccionario donde el id de cada hijo es la key
        diccionario_hijos[hijo[0]] = {
            'nombre':hijo[1],
            'img':hijo[2],
        } 

        # me termina quedando un diccionario de diccionarios
    
    return diccionario_hijos

    
def agregar_solicitud(id_hijo, monto, fecha, estado):
    
    sQuery = """
        INSERT INTO solicitudes(id_usuario, monto, fecha, estado)
        VALUES (%s, %s, %s, %s)
    """

    val = (id_hijo, monto, fecha, estado)
    mydb = conectarDB(BASE)

    try:
        ejecutarDB(mydb, sQuery, val)   # ← IMPORTANTE: ejecutarDB, no consultarDB
        res = True
    except Exception as e:
        print(f"Error en agregar_solicitud: {e}")
        res = False
    finally:
        cerrarDB(mydb)
    return res


def consultar_solicitudes(codfam):

    sQuery = """
        SELECT s.id, s.id_usuario, s.monto, s.fecha, u.nombre_usuario
        FROM solicitudes s
        INNER JOIN usuarios u ON u.id = s.id_usuario
        WHERE s.estado = 'pendiente' AND u.codigo_familiar = %s
        ORDER BY s.fecha DESC
    """

    mydb = conectarDB(BASE)
    lista = consultarDB(mydb, sQuery, (codfam,))
    cerrarDB(mydb)

    # Protección para evitar el TypeError
    solicitudes = []
    if lista != None:

        for sol in lista:
            solicitudes.append({
                'id': sol[0],
                'id_hijo': sol[1],
                'monto': sol[2],
                'fecha': sol[3],
                'nombre_hijo': sol[4]
            })

    return solicitudes

def mis_solicitudes(id):
    sQuery = "SELECT monto, fecha, estado FROM solicitudes WHERE id_usuario = %s ORDER BY fecha DESC LIMIT 5 "
    mydb = conectarDB(BASE)
    lista = consultarDB(mydb, sQuery, (id,))
    cerrarDB(mydb)

    return lista

def obtener_solicitud(id_solicitud):
    sQuery = "SELECT id_usuario, monto, estado FROM solicitudes WHERE id = %s "
    mydb = conectarDB(BASE)
    res = consultarDB(mydb, sQuery, (id_solicitud,))
    cerrarDB(mydb)
    return res[0] if res else None


def actualizar_estado_solicitud(id_solicitud, estado):
    sQuery= "UPDATE solicitudes SET estado = %s WHERE id = %s"
    val = (estado, id_solicitud)
    mydb = conectarDB(BASE)
    res = ejecutarDB(mydb,  sQuery, val)
    cerrarDB(mydb)

    return res


def hijos_pendientes(codfam):
    
    sQuery="SELECT id, nombre_usuario, nombres, apellido FROM usuarios WHERE codigo_Familiar = %s AND es_padre = 0 AND admitido = 0"
    mydb = conectarDB(BASE)
    res = consultarDB(mydb, sQuery, (codfam,))
    cerrarDB(mydb)

    hijos = []
    if res != None:
        for x in res:
            hijos.append({
                'id': x[0],
                'username': x[1],
                'nombre': x[2],
                'apellido': x[3],
            })

    return hijos


def aceptar_hijo(id_hijo):
    query = "UPDATE usuarios SET admitido = 1 WHERE id = %s"
    mydb = conectarDB(BASE)
    ejecutarDB(mydb, query, (id_hijo,))
    cerrarDB(mydb)


def rechazar_hijo(id_hijo):
    query = "DELETE FROM usuarios WHERE id = %s"
    mydb = conectarDB(BASE)
    ejecutarDB(mydb, query, (id_hijo,))
    cerrarDB(mydb)



