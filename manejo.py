
import pandas as pd 
import os 
from matplotlib import pyplot as plt
import  base_datos as db

#direccion, nombre_archivo
def datos_archivos(direccion , gg):
    gg2 = gg.split("@")
    nombre = gg2[1]
    _Name = nombre.split(".")
    Folder_Name = _Name[0]
    nombre = nombre.replace("_", ".")
    nombre_seccio = nombre.split(".")
#aca tambbien 
    nave_linea = nombre_seccio[0].split("_")
#lo que estoy cambiarndo
    # print("La nave {} y linea {}".format(nombre_seccio[0], nombre_seccio[1] ))
    fecha = nombre_seccio[2]
    fecha = fecha[0:8]
    fecha_ral ="".join((fecha[0:4], '-',fecha[4:6], '-',fecha[6:8]) )
    # print("La fecha del archivo es: {}". format(fecha_ral))

    # datos = pd.read_csv('datos/Utilization@N4_L05.202212130000.202212140000.csv')
    datos = pd.read_csv(direccion)
    # datos = pd.read_csv("//gdjnt335/Reportes/N1_L01A/Utilization Daily/2022-12-13/Utilization@N1_L01A.202212130000.202212140000.csv")
    # print(datos)
    modulos = datos.columns.values
    modulos = modulos[1:]
    # print(modulos)
    dd = datos.set_index("Module")
    trans = dd.transpose() 

    trans = trans.assign(Line = nombre_seccio[1])
    trans = trans.assign(Building = nombre_seccio[0])
    trans = trans.assign(Date = fecha_ral)  
    trans = trans.assign(Folder = Folder_Name)
    # print("Despues de asignar el index")

    df_reset = trans.reset_index()
    for x in modulos:
        m3 = df_reset.loc[df_reset['index']== x]
        m4 = m3.to_numpy().tolist()
        #nononono print(m4)
        for y in m4:
            # print(y)
            
            db.insertar_procedires(y)
