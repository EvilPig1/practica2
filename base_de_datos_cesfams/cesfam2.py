import pandas as pd
import sys
import mariadb
from datetime import datetime
import time

def procesamiento(conn):
    # Lee cada hoja y almacena sus datos en el diccionario
    df = pd.read_excel('Informe_Rayen.xlsx',sheet_name=None) #sheet_name = None, transforma todas las hojas del excel en un diccionario

    dataframes = {}
    for sheet_name,dataframe in df.items():
        dataframes[sheet_name] = df[sheet_name].where(pd.notnull(df[sheet_name]), None)
    
    # Accede a los datos de cada hoja usando el diccionario
    for sheet_name, dataframe in dataframes.items():
        for indice, fila in dataframe.iterrows():
            fecha_movimiento = pd.to_datetime(fila['FECHA DE MOVIMIENTO'], format='%Y-%m-%d')#formato 
            valores = list(fila)
            valores[1] = fecha_movimiento.date()  # Convierte a tipo 'date' de Python'''
            db(valores, conn)



def conectar_mariadb(usuario, contra, host_ip, puerto, db):
    try: # conexion tipo de maria db
        conn = mariadb.connect(
            user=usuario,
            password=contra,
            host=host_ip,
            port=puerto,
            database =db
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn


def db(valores, conn):
    curr = conn.cursor()   # insercion de datos dentro de tabla
    curr.execute(
        """INSERT INTO despachos_cesfam(numero_de_receta, fecha_de_movimiento, usuario, establecimiento, sexo,
        escolaridad, pais_de_origen, pueblo_originario, sector, discapacidad, prevision, tipo_receta, articulo,
        posologia_de_la_descripcion, observacion, dosis, cada, unidad_de_tiempo, por, unidad_de_tiempo2, estado_de_receta,
        cantidad_de_despacho, cantidad_sin_despacho, diagnostico, codigo_cie10, edad_años, profesional, sector_inscripcion)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", valores)
    conn.commit()

#programa inicia
inicio = time.time()  #se toma el tiempo total que tomo que se corriera todo el proceso
conn = conectar_mariadb("root","Lom1smo1!","172.30.96.1",3306, "cesfam")
procesamiento(conn)
conn.close()

end = time.time()
elapsed = end - inicio
tiempo_en_minutos = elapsed /60
with open("tiempo.txt","w") as f:
    f.write(str(tiempo_en_minutos) + ": minutos transcurridos desde el traspasando datos desde excel a la base de datos")