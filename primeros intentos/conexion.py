import mariadb #pip3 install mariadb
import sys
from dotenv import load_dotenv
import unicodedata
#import os

#se cargan las variables de entorno
#ruta_env = os.path.abspath(os.path.join(os.path.dirname(__file__), '../.env'))
#load_dotenv(dotenv_path=ruta_env)


def insertaATC(dbconn,file_path):
    curr = dbconn.cursor()
    f = open(file_path,"r")
    for row in f:
        x =row.replace("\n","")
        v = x.split(";")
        v[0]= unicodedata.normalize("NFKD", v[0]).replace(" ","")
        v[1]= unicodedata.normalize("NFKD", v[1]).replace(" ","")
        v[2]= unicodedata.normalize("NFKD", v[2]).strip()
        v[2] = v[2].replace("α", '_')
        v[3]= unicodedata.normalize("NFKD", v[3])
        statement = "INSERT INTO atc(codigo_padre,codigo,nombre,flg_hoja) values(\""+v[0]+"\", '"+v[1]+"',\""+v[2]+"\","+v[3]+" )"
        print(statement)

        cur.execute(statement)
        dbconn.commit()
        print(cur.rowcount,"filas insertadas")

# Connect to MariaDB Platform
try:
    conn = mariadb.connect( # Todos estos datos deberian ser var de entorno
        user="root",
        password="Lom1smo1!", # Es la contrasena que uno define
        host="172.20.78.98",
        port=3306,
        database = "felipe"
    )

except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()


query = "SELECT * FROM ATC"             

cur.execute(query)

rows = cur.fetchall()


print("Aqui se imprimira los codigos atc")
for row in rows:
    print(row)

insertaATC(conn,"datos_2.txt")

conn.close()