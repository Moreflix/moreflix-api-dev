import re
import requests
from bs4 import BeautifulSoup
import urllib.parse
import sys
import os

script_dir = os.path.dirname(__file__)  # Obtiene el directorio del script actual
parent_dir = os.path.dirname(script_dir)  # Obtiene el directorio padre (Api)
scripts_path = os.path.join(parent_dir, 'scripts')  # Construye la ruta al directorio 'scripts'
sys.path.append(scripts_path)

from xmlextract import extract_xml_data

from xmlextract import extract_xml_data

def get_film_data(film_url):
    try:
        req = requests.get(film_url)
        if req.status_code != 200:
            return {"Error": "This media isn't available"}

        html = BeautifulSoup(req.text, "html.parser")
        links = html.find_all('a')
        video_links = []
        nfo_link = None
        info = {}

        video_ext_regex = re.compile(r'.*\.(mp4|MP4|avi|AVI|mpg|MPG|mkv|MKV)$')
        nfo_ext_regex = re.compile(r'.*\.nfo$')

        nfo_found = False

        for link in links:
            href = link.get('href')
            if href:
                if video_ext_regex.match(href):
                    full_url = urllib.parse.urljoin(film_url, href)
                    video_links.append(full_url)
                elif nfo_ext_regex.match(href):
                    nfo_link = urllib.parse.urljoin(film_url, href)
                    info = extract_xml_data(nfo_link)
                    info["Source"] = video_links
                    nfo_found = True
                    break

        return info

    except Exception as e:
        return {"Error": f"Error getting the media information: {e}"}