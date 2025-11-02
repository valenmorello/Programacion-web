#EJEMPLO
sQuery= """
    INSERT INTO base
    (id, nombre, apellido, email, pass)
    VALUES
    (%s,%s,%s,%s,%s,)
"""
val = ("valor1","valor2","valor3","valor4") #el execute reemplaza los valores