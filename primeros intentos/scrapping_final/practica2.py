from bs4 import BeautifulSoup
import requests
import bs4

def productos(href,url2):
    cadena = "/resource/atc/"
    if(cadena in href):
        URL_PRODUCTOS = url2+href
    else:
       URL_PRODUCTOS = url2+cadena+href
    url_b = url2 
    print(URL_PRODUCTOS)
    producto = requests.get(URL_PRODUCTOS)
    HTML_OBT =producto.text

    sopa = BeautifulSoup(HTML_OBT,"html.parser")
    div_p_list = sopa.find('div', {'class': 'p-list'})

    if div_p_list:

        li_list = div_p_list.find_all("li")

        resultado = {}
        hrefs = []
        for elemento in li_list:
            etiqueta = elemento.get_text(strip=True, separator=' ').split(' ')[0]
            enlace = elemento.find('a', {'class': 'blue fb'})
            texto_enlace = enlace.get_text() if enlace else ''
            resultado[etiqueta] = texto_enlace.strip()
        
        for e in enlace:
            href2 = enlace.get("href")
            hrefs.append(href2) #aqui le paso cada una de los link al siguiente producto
        
        with open("datos.txt","a") as f:
            for key, value  in resultado.items():
                f.write(f"{key}: {value}\n")
        
        for h in hrefs:
            productos(h,url_b)

    else:
        print("no existes")
        
       

    

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


        

'''
URL_BASE = 'https://www.chemnet.com/resource/atc/'
pedido_obtenido = requests.get(URL_BASE)
html_obtenido = pedido_obtenido.text


#es necesario hacer esto
soup = BeautifulSoup(html_obtenido,"html.parser")


# Encuentra el div con la clase "p-list"
div_p_list = soup.find_all('div', {'class': 'p-list'})

if div_p_list:
    # Encuentra la lista ul dentro del div
    li_list = div_p_list.find_all('li')

    for li in li_list:
        texto = li.get_text(strip=True)
        print(texto)

else:
    print("no existess")

'''
