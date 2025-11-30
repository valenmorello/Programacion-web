import mysql.connector
import mysql.vendor

BASE={ "host":"mysql-tomasmaraval.alwaysdata.net", 
      "user":"437721",
      "pass":"canalla06",
      "dbname":"tomasmaraval_familybank"
}

def conectarDB (configDB=None):
    mydb=None
    if configDB!=None:
        try:
            mydb = mysql.connector.connect(
            host = configDB.get("host"),
            user = configDB.get("user"),
            password = configDB.get("pass"),
            database = configDB.get("dbname"), 
        )
        except mysql.connector.Error as e:
            print("Error -->", e)
    return mydb

def cerrarDB(mydb):
    if mydb!=None:
        mydb.close()

def consultarDB(mydb,sQuery="", val=None, title=False):  #recibe la consulta y los valores por separado
    myresult = None
    try: 
        if mydb!=None:
            mycursor = mydb.cursor()     #espacio de memoria local donde almaceno la base
            if val == None:
                mycursor.execute(sQuery)
            else:
                mycursor.execute(sQuery,val)
            myresult = mycursor.fetchall()                  
            
            if title:
                myresult.insert(0,mycursor.column_names)
    except mysql.connector.Error as e:
        print("Error-->",e)
    return myresult

def ejecutarDB(mydb,sQuery="",val=None):
    res=None
    try:
        mycursor = mydb.cursor()
        if val==None:
            mycursor.execute(sQuery)
        else:
            mycursor.execute(sQuery,val)
        mydb.commit()   
        ###res=mycursor.rowcount        # filas afectadas
        res = mycursor.lastrowid  
    except mysql.connector.Error as e:
        mydb.rollback()
        print("ERROR ->",e)    
    return res #retorna las filas afectadas



#FLASK, Direcciones locales


