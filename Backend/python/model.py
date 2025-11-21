from mysql_db import *
import random

# ------ VALIDAR LOGIIIINNNNNN ---------------

def validar_login (dic, username, password):
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

def existe_usuario (nombre_usuario):
    sQuery="""
        SELECT nombre_usuario FROM usuarios WHERE nombre_usuario = %s """
    val = (nombre_usuario,)
    mydb = conectarDB(BASE)
    res = consultarDB(mydb,sQuery,val)
    cerrarDB(mydb)

    return len(res) > 0

def existe_codfam (codfam):
    sQuery="""
        SELECT codigo_Familiar FROM usuarios WHERE codigo_Familiar = %s """
    val = (codfam,)
    mydb = conectarDB(BASE)
    res = consultarDB(mydb,sQuery,val)
    cerrarDB(mydb)

    return len(res) > 0

def registro(nombre, apellido, codfam, es_padre, contrasenia, nombre_usuario, img, admitido=0, saldo=0):
    res = None
    if not existe_usuario(nombre_usuario):  
        if es_padre == 1:
            admitido = 1

            codfam = random.randint(100000, 999999)
            while existe_codfam(codfam):
                codfam = random.randint(100000, 999999)

            sQuery="""
            INSERT INTO usuarios
            (id, nombres, apellido, codigo_Familiar, es_padre, saldo, contrasenia, nombre_usuario, admitido, img)
            VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            val = (None, nombre, apellido, codfam, es_padre, saldo, contrasenia, nombre_usuario, admitido, img,)
            mydb = conectarDB(BASE)
            res = ejecutarDB(mydb, sQuery,val)
            cerrarDB(mydb)  
    return res

def modificarnombre(id, nuevonombre):
    sQuery="UPDATE usuarios SET nombres=%s WHERE id=%s"
    val = (nuevonombre, id)
    mydb=conectarDB(BASE)
    res = ejecutarDB(mydb,sQuery,val)       # update
    cerrarDB(mydb)
    return res

def modificarapellido(id, nuevoape):
    sQuery="UPDATE usuarios SET apellido=%s WHERE id=%s"
    val = (nuevoape, id)
    mydb=conectarDB(BASE)
    res=ejecutarDB(mydb,sQuery,val)       # update
    cerrarDB(mydb)
    return res


# ---- PLATA ------

def saldoactual(nombre_usuario):
    sQuery="SELECT saldo FROM usuarios WHERE nombre_usuario=%s"
    val = (nombre_usuario,)
    mydb = conectarDB(BASE)
    res = consultarDB(mydb,sQuery,val)
    cerrarDB(mydb)
    return res

def find_id (nombre_usuario,):
    sQuery="SELECT id FROM usuarios WHERE nombre_usuario=%s"
    val = (nombre_usuario,)
    mydb = conectarDB(BASE)
    res = consultarDB(mydb,sQuery,val)
    cerrarDB(mydb)
    return res

def transferencia(usuario_emisor, usuario_receptor, monto, motivo, fecha):
    res = None
    id_emisor = find_id(usuario_emisor)
    id_receptor = find_id(usuario_receptor)

    saldoemisor = saldoactual(usuario_emisor)
    saldoreceptor = saldoactual(usuario_receptor)
    
    if saldoemisor >= monto:
        saldoemisor = saldoemisor - monto
        saldoreceptor = saldoreceptor + monto

        sQuery ="""
        UPDATE usuario SET 'saldo'=%s WHERE nombre_usuario=%s
        UPDATE usuario SET 'saldo'=%s WHERE nombre_usuario=%s

        INSERT INTO actividad
        (id, emisor, receptor, motivo, fecha, monto)
        VALUES
        (Null,%s,%s,%s,%s,%s)
        """
        val = (saldoemisor, usuario_emisor, saldoreceptor, usuario_receptor,
                id_emisor, id_receptor,motivo,fecha,monto)
        
        mydb=conectarDB(BASE)
        res=ejecutarDB(mydb,sQuery,val)      
        cerrarDB(mydb)

    return res

# ------ HIJOOOOOOSSSSSSS -----------------------------------------------------------

# devuelve una lista de tuplas, cada elemento de la lista es un hijo. 

def encontrar_hijos(codfam):
    sQuery="SELECT * FROM usuarios WHERE codigo_Familiar=%s and es_padre=0 and admitido=1"
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
            'apellido':hijo[2],
            'saldo':hijo[5],
            'usuario':hijo[7],
            'img':hijo[9],
        } 

        print (diccionario_hijos)
        # me termina quedando un diccionario de diccionarios
    return diccionario_hijos

def buscar_hijo_en_bd(id_hijo, cf):
    sQuery="SELECT * FROM usuarios WHERE id=%s and codigo_Familiar=%s and admitido=1"
    val = (id_hijo, cf,)
    mydb = conectarDB(BASE)
    fila = consultarDB(mydb,sQuery,val) #lista de tuplas
    cerrarDB(mydb)

    dic = {}
    if fila!=[]:
        res=True
        dic['id']=fila[0][0]
        dic['nombre']=fila[0][1]
        dic['apellido']=fila[0][2]
        dic['saldo']= fila[0][5]
        dic['nombre_usuario']=fila[0][7]
        dic['img']=fila[0][9]

    return dic