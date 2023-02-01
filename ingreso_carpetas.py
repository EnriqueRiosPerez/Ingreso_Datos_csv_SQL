import os
import os.path
import base_datos as db
import manejo as manage
lista_existente = []
lista_no_existente = []
# from base_datos import consulta 
content = os.listdir('/Users/gdjenrio/Documents/Almacen Central/Acciones-CLCA')
direccion_reportes= '//gdjnt335/Reportes/'

carpeta_utilizacion = "Utilization Daily"
lista_carpetas = os.listdir('//gdjnt335/Reportes/')
# \\gdjnt335\Reportes\N4_L05\Utilization Daily
os.chdir(direccion_reportes)
print("la direccion {}" .format(os.getcwd()))

for x in lista_carpetas:
    print(x)
    direccion_carpetas = (os.path.join(direccion_reportes,x))
    # print(direccion_carpetas)
    os.chdir(direccion_carpetas)
    # print("la direccion {}" .format(os.getcwd()))
    if os.path.exists(carpeta_utilizacion):
        lista_existente.append(x)
        
        direccion_carpetas_utili = (os.path.join(direccion_carpetas + "/",carpeta_utilizacion))
        print(direccion_carpetas_utili)
        os.chdir(direccion_carpetas_utili)
        fechas = os.listdir(".")
        # print("la direccion {}" .format(os.getcwd()))
        # print("Las fechas que tiene el archivo: {}".format(fechas))
        for carpetas_fechas in fechas:
            dd = os.path.join(direccion_carpetas_utili + "/", carpetas_fechas)
            os.chdir(dd)
            # print("la direccion {}" .format(os.getcwd()))
            archivos_modificacion = os.listdir(".")
            #print("Archivos de fecha {} : {}" .format(carpetas_fechas,archivos_modificacion ))
            validacion = db.consulta(x,carpetas_fechas)
            # print("Validacion si existe de algun registro {}" .format(validacion))
            if validacion == 0:
                print("Archivo no existente")
                for rr in archivos_modificacion:
                    if "Utilization" in rr:
                        nombre_archivo = rr
                        break
                full_path = os.path.join(dd + "/", nombre_archivo)
                print("El archivo que se mandara {}". format(nombre_archivo))
                print("Direccion completa para mandar el archivo: \n{}".format(full_path))
                manage.datos_archivos(full_path,nombre_archivo)
                
            else:
                print("Ya se mando el archivo")       
            os.chdir(direccion_carpetas_utili)
            # print("la direccion despues{}" .format(os.getcwd()))

    else:
        lista_no_existente.append(x)
        print("No se tiene registro de esa carpeta")


print("De las {} carpetas, {} si tienen el archivo y {} no la tienen " .format(len(lista_carpetas),len(lista_existente ), len(lista_no_existente)))
print("Carpetas que no tienen el archivo: {}" .format(lista_no_existente))