import os
# import os.path
import pyodbc
import pandas as pd 
from matplotlib import pyplot as plt
# import base_datos as db
# import manejo as manage
lista_existente = []
lista_no_existente = []
mandados = 0
no_mandados = 0
archivos_nuevos = 0 
c_origen= "//gdjnt335/Reportes/"
c_utilizacion = "Utilization Daily"
lista_c_utilizacion = os.listdir(c_origen)
os.chdir(c_origen)
# print("La direccion {}" .format(os.getcwd()))



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


def datos_archivos(direccion , N_L, fecha):
    n,l = N_L.split("_")
    datos = pd.read_csv(direccion)
    modulos = datos.columns.values
    modulos = modulos[1:]
    dd = datos.set_index("Module")
    trans = dd.transpose() 
    trans = trans.assign(Line = l)
    trans = trans.assign(Building = n)
    trans = trans.assign(Date = fecha)  
    trans = trans.assign(Folder = N_L)
    df_reset = trans.reset_index()
    for x in modulos:
        m3 = df_reset.loc[df_reset['index']== x]
        m4 = m3.to_numpy().tolist()
        #nononono print(m4)
        for y in m4:
            # print(y)
            insertar_procedires(y)




for x in lista_c_utilizacion:
    print(x)
    direccion_carpetas = (os.path.join(c_origen,x))
    os.chdir(direccion_carpetas)
    if os.path.exists(c_utilizacion):

        lista_existente.append(x)
        no_mandados = no_mandados+1
        direccion_c_utilizacion = (os.path.join(direccion_carpetas + "/",c_utilizacion))
        # print(direccion_c_utilizacion)
        os.chdir(direccion_c_utilizacion)
        c_fechas = os.listdir(".")

        for fechas in c_fechas:
            direccion_fechas = os.path.join(direccion_c_utilizacion + "/", fechas)
            os.chdir(direccion_fechas)
            lista_archivos = os.listdir(".")

            validacion = consulta(x,fechas)



            if validacion == 0:
                # print("Archivo no existente")
                for file_name in lista_archivos:
                    if "Utilization" in file_name:
                        nombre_archivo = file_name
                        break
                full_path = os.path.join(direccion_fechas + "/", nombre_archivo)
                # print("El archivo que se mandara {}". format(nombre_archivo))
                # print("Direccion completa para mandar el archivo: \n{}".format(full_path))
                archivos_nuevos = archivos_nuevos+1
                #direccion completa al archivo para ingrsar los datos , x  es el nombre de la carpeta en la que se esta trabajando,
                # fechas es el nombre de la carpeta que tiene fecha  
                datos_archivos(full_path,x,fechas)
            else:
                # print("Ya se mando el archivo")
                mandados = mandados+1       
            os.chdir(direccion_c_utilizacion)
    else:
        lista_no_existente.append(x)
        # print("No se tiene la carpeta {}" .format(c_utilizacion))


print("De las {} carpetas, {} si tienen el archivo y {} no la tienen " .format(len(lista_c_utilizacion),len(lista_existente ), len(lista_no_existente)))
print("Se reportaron {} archivos nuevos y se tenian {}" .format(archivos_nuevos, mandados))
print("Carpetas que no tienen el archivo: {}" .format(lista_no_existente))