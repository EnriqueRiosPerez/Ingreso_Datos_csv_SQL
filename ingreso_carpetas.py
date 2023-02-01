import os
import os.path
import base_datos as db
import manejo as manage
lista_existente = []
lista_no_existente = []
mandados = 0
no_mandados = 0
archivos_nuevos = 0 
c_origen= "//gdjnt335/Reportes/"
c_utilizacion = "Utilization Daily"
lista_c_utilizacion = os.listdir(c_origen)
os.chdir(c_origen)
print("La direccion {}" .format(os.getcwd()))

for x in lista_c_utilizacion:
    print(x)
    direccion_carpetas = (os.path.join(c_origen,x))
    os.chdir(direccion_carpetas)
    if os.path.exists(c_utilizacion):

        lista_existente.append(x)
        no_mandados = no_mandados+1
        direccion_c_utilizacion = (os.path.join(direccion_carpetas + "/",c_utilizacion))
        print(direccion_c_utilizacion)
        os.chdir(direccion_c_utilizacion)
        c_fechas = os.listdir(".")

        for fechas in c_fechas:
            direccion_fechas = os.path.join(direccion_c_utilizacion + "/", fechas)
            os.chdir(direccion_fechas)
            lista_archivos = os.listdir(".")
            validacion = db.consulta(x,fechas)
            if validacion == 0:
                print("Archivo no existente")
                for file_name in lista_archivos:
                    if "Utilization" in file_name:
                        nombre_archivo = file_name
                        break
                full_path = os.path.join(direccion_fechas + "/", nombre_archivo)
                print("El archivo que se mandara {}". format(nombre_archivo))
                print("Direccion completa para mandar el archivo: \n{}".format(full_path))
                archivos_nuevos = archivos_nuevos+1
                #direccion completa al archivo para ingrsar los datos , x  es el nombre de la carpeta en la que se esta trabajando,
                # fechas es el nombre de la carpeta que tiene fecha  
                manage.datos_archivos(full_path,x,fechas)
            else:
                print("Ya se mando el archivo")
                mandados = mandados+1       
            os.chdir(direccion_c_utilizacion)
    else:
        lista_no_existente.append(x)
        print("No se tiene la carpeta {}" .format(c_utilizacion))


print("De las {} carpetas, {} si tienen el archivo y {} no la tienen " .format(len(lista_c_utilizacion),len(lista_existente ), len(lista_no_existente)))
print("Se reportaron {} archivos nuevos y se tenian {}" .format(archivos_nuevos, mandados))
print("Carpetas que no tienen el archivo: {}" .format(lista_no_existente))