import mariadb
from bs4 import BeautifulSoup
import requests
import bs4
import time


def productos(URL_BASE, HREF, Href_padre):
   
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
            with open("datos_3.txt","a") as f:
                if(etiqueta_td[0].text.strip()):
                    f.write(Href_padre+" ;")
                    f.write(etiqueta_td[0].text+";")
                    f.write(etiqueta_td[1].text+";1\n")

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
            with open("datos_3.txt","a") as f:
                f.write(Href_padre+" ;")
                f.write(shref4 +" ;")
                f.write(j.text+" ;0\n")
            productos(URL_BASE2, shref2, shref4)
        
    

#codigo padre; codigo hijo; texto; 0 ó 1

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
        productos(URL_BASE, shref, padre)