import re
import requests
from bs4 import BeautifulSoup
import urllib
import time

def extract_media_info(url):
    try:
        req = requests.get(url)
        statusCode = req.status_code
        if statusCode != 200:
            return None  # O manejar el error como prefieras

        html = BeautifulSoup(req.text, "html.parser")
        enlaces = html.find_all('a')

        parent_directory_url = None
        subtitulo = None
        portada = None
        nombre_serie = url.split('/')[-3]
        temporada = url.split('/')[-2]

        for enlace in enlaces:
            href = enlace.get('href')
            text = enlace.string
            if text == 'Parent Directory':
                parent_directory_url = urllib.parse.urljoin(url, href)
            elif text not in ['Name', 'Last modified', 'Size', 'Description', 'ayuda']:
                if href and (href.endswith('.srt')):
                    subtitulo = urllib.parse.urljoin(url, href)
                elif href and (href.endswith('.jpg')):
                    portada = urllib.parse.urljoin(url, href)

        return {
            'parent_directory_url': parent_directory_url,
            'subtitulo': subtitulo,
            'portada': portada,
            'nombre_serie': nombre_serie,
            'temporada': temporada
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

# Ejemplo de uso
url = "http://example.com/series/temporada1/"
info = extract_media_info(url)
if info:
    print(info)
else:
    print("No se pudo extraer la información.")