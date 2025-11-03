from BD import *

def registro(usuario, nombre, apellido, codfam, contraseña):
    sQuery="""
        INSERT INTO usuario
        (usuario, nombre, apellido, codfam, contraseña)
        VALUES
        (%s,%s,%s,%s,%s,)"""
    val = (usuario, nombre, apellido, codfam, contraseña)
    mydb = conectarDB(BASE)
    res = ejecutarDB(mydb, sQuery,val)
    cerrarDB(mydb)
    return res

def usuario_existe():
    pass #COMPLETAR

def modificarnombre(usuario, nuevonombre):
    sQuery="UPDATE usuario SET 'nombre'=%s WHERE usuario=%s"
    val = (nuevonombre, usuario)
    mydb=conectarDB(BASE)
    res=ejecutarDB(mydb,sQuery,val)       # update
    cerrarDB(mydb)
    return res

def modificarapellido(usuario, nuevoape):
    sQuery="UPDATE usuario SET 'apellido'=%s WHERE usuario=%s"
    val = (nuevoape, usuario)
    mydb=conectarDB(BASE)
    res=ejecutarDB(mydb,sQuery,val)       # update
    cerrarDB(mydb)
    return res


    