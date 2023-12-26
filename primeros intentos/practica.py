from bs4 import BeautifulSoup
import requests
import bs4


def productos(href, url2):
    URL_PRODUCTOS = url2+href
    url_b = url2
    print(URL_PRODUCTOS)
    producto = requests.get(URL_PRODUCTOS)
    HTML_OBT =producto.text

    sopa = BeautifulSoup(HTML_OBT,"html.parser")
    elementos_ul = sopa.find_all('ul')
  
    resultado = {}
    hrefs = []
    elementos_il = elementos_ul[2].find_all('li')

    for elemento in elementos_il:
        etiqueta = elemento.get_text(strip=True, separator=' ').split(' ')[0]
        enlace = elemento.find('a', {'class': 'blue fb'})
        texto_enlace = enlace.get_text() if enlace else ''
        resultado[etiqueta] = texto_enlace.strip()

    for e in enlace:
        href = enlace.get("href")
        hrefs.append(href) #aqui le paso cada una de los link al siguiente producto
    
    for h in hrefs:
        confirmar = url2 +"/resource/atc/"+ h
        productos2(confirmar)

    with open("datos.txt","a") as f:
        for key, value  in resultado.items():
            f.write(f"{key}: {value}\n")
    

def productos2(confirmar):
    URL_PRODUCTOS = confirmar
    print(URL_PRODUCTOS)
    producto = requests.get(URL_PRODUCTOS)
    HTML_OBT =producto.text

    sopa = BeautifulSoup(HTML_OBT,"html.parser")
    elementos_ul = sopa.find_all('ul')
  
    resultado = {}
    elementos_il = elementos_ul[2].find_all('li')

    for elemento in elementos_il:
        etiqueta = elemento.get_text(strip=True, separator=' ').split(' ')[0]
        enlace = elemento.find('a', {'class': 'blue fb'})
        texto_enlace = enlace.get_text() if enlace else ''
        resultado[etiqueta] = texto_enlace.strip()

    with open("archivo.txt","a") as f:
        for key, value  in resultado.items():
            f.write(f"{key}: {value}\n")
    





URL_BASE = 'https://www.chemnet.com/resource/atc/'
pedido_obtenido = requests.get(URL_BASE)
html_obtenido = pedido_obtenido.text


#es necesario hacer esto
soup = BeautifulSoup(html_obtenido,"html.parser")

hrefs = [] # lista vacia para 
enlaces = soup.find_all('a', {'class': 'blue fb fftt'})
url2 = 'https://www.chemnet.com'
for enlace in enlaces:
    href = enlace.get("href")
    hrefs.append(href) #aqui le paso cada una de los link al siguiente producto

for h in hrefs:
    productos(h,url2)


        