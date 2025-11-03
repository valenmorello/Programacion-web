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
    cerrarBD(mydb)
    return res


