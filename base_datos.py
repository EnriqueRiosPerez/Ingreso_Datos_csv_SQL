import pyodbc

def cn():
    #se crean las variables de conexion 
    server = 'gdjnt280\FIREPORT'
    base_datos = 'Maintenance_Management'
    usuario = 'ProdUser'
    password = 'Pr0dUs@r'
    try:
        # se genera la conexion a la base de datos
        conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server+';DATABASE='+base_datos+';UID='+usuario+';PWD=' + password)
        #ingresa si es exitosa 
        # print("Conexion exitosa")
        
    except Exception as e:
        #Asi muestra el error
        print("Ocurrió un error al conectar a SQL Server: ", e)
    return conexion

def insertar_procedires(datos):
    conexion = cn()
    cursor = conexion.cursor()
    comando = "exec insert_Module_data @Module = ? , @Production =  ?,  @Wait_Previous = ?, @Wait_Next = ?, @Changeover = ?, @Part_Supply = ?, @Machine_Error = ? , @Operator_Downtime = ?, @Maintenance = ?, @Other = ?, @Line = ?,  @Building = ?, @Date = ? , @Folder_Name = ?"
    cursor.execute(comando, datos[0], datos[1], datos[2], datos[3], datos[4], datos[5], datos[6], datos[7], datos[8], datos[9], datos[10], datos[11], datos[12], datos[13])
    cursor.commit()
    cursor.close()
    conexion.close()  
    # print("Se actualizaron correctamente los registros")
def consulta(Folder, Date):
    conexion =  cn()
    cursor = conexion.cursor()
    try:
        comando = "Select DISTINCT  Folder_Name from [dbo].Mantenimiento_Module_data where Date = ? and Folder_Name = ?"
        cursor.execute(comando, Date,Folder)
        #DISTINCT 
    except Exception as e:
         print("Error de conexion: ", e)
    #se crea una variable usuarios para guardar lo que se encuentra en la tabla y lo muestra
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    return len(usuarios)
