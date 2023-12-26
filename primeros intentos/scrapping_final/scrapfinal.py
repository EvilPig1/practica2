import sys
from bs4 import BeautifulSoup
import requests
import bs4
import time
import unicodedata
import mariadb

def productos(conn,URL_BASE, HREF, Href_padre):
   
    URL_NUEVA = URL_BASE+ HREF
    pedido_nuevo = requests.get(URL_NUEVA)
    HTML_obt = pedido_nuevo.text
    URL_BASE2 = URL_BASE

    sopa = BeautifulSoup(HTML_obt, "html.parser")

    etiqueta_content = sopa.find('div', {'id': 'content'})
    etiqueta_ul = etiqueta_content.find('ul')
    etiqueta_p= etiqueta_content.find_all('p')

    etiquetas_b2 = etiqueta_p[1].find_all('b')
    
    if(etiqueta_ul):
        etiqueta_tr= etiqueta_ul.find_all('tr')
        etiqueta_tr2 = etiqueta_tr[1:]
        for t in etiqueta_tr2:
            etiqueta_td = t.find_all('td', limit = 2)
            etiqueta1=unicodedata.normalize("NFKD", str(etiqueta_td[0].text)).strip()
            etiqueta2=unicodedata.normalize("NFKD", str(etiqueta_td[1].text))
            td_a=etiqueta_td[1].find("a")
            if td_a:
                tdhref= td_a.get("href")
                tdhref2 = tdhref[2:]
                tdhref3 = URL_BASE+tdhref2
                hoja= 1
                value = None
                conexion(conn,Href_padre,etiqueta1,URL_NUEVA,tdhref3,value,etiqueta2,hoja)
                if(tdhref is None):
                    tdhref=""
            with open("datos.txt","a") as f:
                if(etiqueta_td[0].text.strip()):
                    f.write(Href_padre+";"+etiqueta1+";"+URL_NUEVA+" ;"+tdhref3+" ;"+etiqueta2+";"+str(hoja)+"\n")

    else:
        for j in etiquetas_b2:
            etiquetas_a2 = j.find_all('a')
            for etiqueta_a2 in etiquetas_a2:
                href2 = etiqueta_a2.get('href')
                time.sleep(1)
                shref2 = href2[2:]
                shref3 = shref2[6:]
                posicion = shref3.find("&")
                shref4 =shref3[:posicion]
                texto=unicodedata.normalize("NFKD",str(j.text))
                value = None
                rama = 0
            conexion(conn,Href_padre,shref4,URL_NUEVA,value,value,texto,rama)
            with open("datos.txt","a") as f:
                f.write(Href_padre+";"+shref4+";"+URL_NUEVA+" ;"+str(value)+";"+texto+";"+str(rama)+"\n")
            productos(conn,URL_BASE2, shref2, shref4)


def conexion(conn,codigo_padre,codigo_hijo,URL,URL_Medicamento,Descripcion,Contexto,hoja):
    Contexto = Contexto.replace("α", '_')
    cur = conn.cursor()

    cur.execute(
                "INSERT INTO codigo_atc (codigo_padre, codigo_hijo, link_atc, link_medicamento, descripcion, path_contexto,flag_hoja) VALUES (%s, %s, %s, %s, %s, %s,%s)",
                (
                    codigo_padre,
                    codigo_hijo,
                    URL,
                    URL_Medicamento,
                    Descripcion,
                    Contexto,
                    hoja
                ),
            )
    conn.commit()
        
    

try:
        conn = mariadb.connect( # Todos estos datos deberian ser var de entorno
            user="root",
            password="Lom1smo1!", # Es la contrasena que uno define
            host="192.168.182.149",
            port=3306,
            database = "felipe"
        )

except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

URL_BASE = 'https://www.whocc.no/atc_ddd_index/'
pedido_obtenido = requests.get(URL_BASE)
html_obtenido = pedido_obtenido.text

soup = BeautifulSoup(html_obtenido,"html.parser")

etiqueta_content = soup.find('div', {'id': 'content'})
etiqueta_p2= etiqueta_content.find_all('p')

etiquetas_b= etiqueta_p2[1].find_all('b')
    
for etiqueta_b in etiquetas_b:
    etiqueta_a = etiqueta_b.find('a')
    if etiqueta_a: 
        href = etiqueta_a.get('href')
        shref = href[2:]
        shref5 = href[8:]
        padre =  shref5[0]
        productos(conn,URL_BASE, shref, padre)

conn.close()


#ver modelos de datos relacionales.
#diagrama entidad relacional atributos
#diagrama