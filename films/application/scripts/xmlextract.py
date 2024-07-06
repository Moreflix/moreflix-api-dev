import requests
from bs4 import BeautifulSoup

def extract_xml_data(url):
    # Realizar la petición HTTP para obtener el contenido del archivo
    response = requests.get(url)
    content = response.content

    # Parsear el contenido XML
    soup = BeautifulSoup(content, 'lxml-xml')

    # Extraer la información deseada
    title = soup.find('title').text or soup.find('originaltitle').text
    director = soup.find('director').text
    plot_cdata = soup.find('plot').text
    year = soup.find('year').text
    genre = soup.find('genre').text
    country = soup.find('country').text
    studio = soup.find('studio').text

    # Extraer el texto después de "<![CDATA[" y antes de "]]>"
    plot_text = plot_cdata.split("<![CDATA[")[-1].split("]]>")[0]

    # Devolver los resultados como un diccionario
    return {
        "Title": title,
        "Director": director,
        "Plot": plot_text,
        "Year": year,
        "Genre": genre,
        "Country": country,
        "Studio": studio
    }