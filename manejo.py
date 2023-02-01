
import pandas as pd 
from matplotlib import pyplot as plt
import  base_datos as db


                                            
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
            db.insertar_procedires(y)