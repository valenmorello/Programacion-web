from mysql_db import *
import random

# ------ VALIDAR LOGIIIINNNNNN ---------------

def validar_login (dic, username, password):
    res=False
    sQuery="""
    SELECT * 
    FROM  usuarios WHERE  nombre_usuario=%s and contrasenia=%s;"""
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

    if res == []:
        res = False
    else:
        res = True
    return res

def existe_codfam (codfam):
    sQuery="""
        SELECT codigo_Familiar FROM usuarios WHERE codigo_Familiar = %s """
    val = (codfam,)
    mydb = conectarDB(BASE)
    res = consultarDB(mydb,sQuery,val)
    cerrarDB(mydb)

    if res == []:
        res = False
    else:
        res = True
    return res

def registro(nombre, apellido, codfam, es_padre, contrasenia, nombre_usuario, img, admitido=0, saldo=0):
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
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,)"""
            val = ('Null', nombre, apellido, codfam, es_padre, saldo, contrasenia, nombre_usuario, admitido, img,)
            mydb = conectarDB(BASE)
            res = ejecutarDB(mydb, sQuery,val)
            cerrarDB(mydb)  
    return res


def modificarnombre(nombre_usuario, nuevonombre):
    sQuery="UPDATE usuarios SET nombres=%s WHERE nombre_usuario=%s"
    val = (nuevonombre, nombre_usuario)
    mydb=conectarDB(BASE)
    res = ejecutarDB(mydb,sQuery,val)       # update
    cerrarDB(mydb)
    return res

def modificarapellido(nombre_usuario, nuevoape):
    sQuery="UPDATE usuarios SET apellido=%s WHERE nombre_usuario=%s"
    val = (nuevoape, nombre_usuario)
    mydb=conectarDB(BASE)
    res=ejecutarDB(mydb,sQuery,val)       # update
    cerrarDB(mydb)
    return res


# ---- PLATA ------

def saldoactual(nombre_usuario):
    sQuery="SELECT saldo FROM usuarios WHERE nombre_usuario=%s"
    val = (nombre_usuario)
    mydb = conectarDB(BASE)
    res = consultarDB(mydb,sQuery,val)
    cerrarDB(mydb)
    return res

def find_id (nombre_usuario):
    sQuery="SELECT id FROM usuarios WHERE nombre_usuario=%s"
    val = (nombre_usuario)
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




