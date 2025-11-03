from BD import *

def registro(nombre_usuario, nombre, apellido, codfam, contrasenia):
    sQuery="""
        INSERT INTO usuario
        (nombre_usuario, nombres, apellido, codigofamiliar, contrasenia)
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
    sQuery="UPDATE usuario SET nombres=%s WHERE nombre_usuario=%s"
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

def verificacion_de_ususario(usuario_receptor):
    sQuery="""
    SELECT nombre FROM usuario WHERE nombre_usuario=%s
    SELECT apellido FROM usuario WHERE nombre_usuario=%s
    """
    val = (usuario_receptor,usuario_receptor)
    mydb = conectarDB(BASE) 
    res = consultarDB(mydb,sQuery,val)
    cerrarDB(mydb)
    return res

def transferencia(usuario_emisor, usuario_receptor, monto):
    res = None
    saldoemisor = saldoactual(usuario_emisor)
    saldoreceptor = saldoactual(usuario_receptor)
    
    if saldoemisor >= monto:
        saldoemisor = saldoemisor - monto
        saldoreceptor = saldoreceptor + monto

        sQuery ="""
        UPDATE usuario SET 'saldo'=%s WHERE nombre_usuario=%s
        UPDATE usuario SET 'saldo'=%s WHERE nombre_usuario=%s
        """
        val = (saldoemisor, usuario_emisor, saldoreceptor, usuario_receptor)
        mydb=conectarDB(BASE)
        res=ejecutarDB(mydb,sQuery,val)      
        cerrarDB(mydb)

    return res





    
    