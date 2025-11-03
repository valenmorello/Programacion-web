from BD import *

def obtener_datos(dato, tabla, columna, valor):
    sQuery="SELECT {} FROM {} WHERE {}=%s".format(dato,tabla,columna)
    val = (valor)
    mydb = conectarDB(BASE)
    res = consultarDB(mydb,sQuery,val)
    cerrarDB(mydb)
    return res

def registro(nombre_usuario, nombre, apellido, codfam, contrasenia):
    sQuery="""
        INSERT INTO usuario
        (Null, nombre_usuario, nombres, apellido, codigofamiliar, contrasenia)
        VALUES
        (%s,%s,%s,%s,%s,)"""
    val = (nombre_usuario, nombre, apellido, codfam, contrasenia)
    mydb = conectarDB(BASE)
    res = ejecutarDB(mydb, sQuery,val)
    cerrarDB(mydb)
    return res

def usuario_existe():
    pass #COMPLETAR

def modificarnombre(nombre_usuario, nuevonombre):
    sQuery="UPDATE `usuario` SET nombres=%s WHERE nombre_usuario=%s"
    val = (nuevonombre, nombre_usuario)
    mydb=conectarDB(BASE)
    res=ejecutarDB(mydb,sQuery,val)       # update
    cerrarDB(mydb)
    return res

def modificarapellido(nombre_usuario, nuevoape):
    sQuery="UPDATE usuario SET apellido=%s WHERE nombre_usuario=%s"
    val = (nuevoape, nombre_usuario)
    mydb=conectarDB(BASE)
    res=ejecutarDB(mydb,sQuery,val)       # update
    cerrarDB(mydb)
    return res

# ---- PLATA ------

def saldoactual(nombre_usuario):
    sQuery="SELECT saldo FROM usuario WHERE nombre_usuario=%s"
    val = (nombre_usuario)
    mydb = conectarDB(BASE)
    res = consultarDB(mydb,sQuery,val)
    cerrarDB(mydb)
    return res

def transferencia(usuario_emisor, usuario_receptor, monto, motivo, fecha):
    res = None
    id_emisor = obtener_datos("id","usuario","nombre_usuario",usuario_emisor)
    id_receptor = obtener_datos("id","usuario","nombre_usuario",usuario_receptor)

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




    
    