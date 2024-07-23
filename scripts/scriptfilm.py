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
        cover_link = None
        nfo_link = None
        subtitle_link = None
        info = {}

        video_ext_regex = re.compile(r'.*\.(mp4|MP4|avi|AVI|mpg|MPG|mkv|MKV)$')
        nfo_ext_regex = re.compile(r'.*\.nfo$')
        cover_found = False
        nfo_found = False
        subtitle_found = False

        for link in links:
            href = link.get('href')
            if href:
                if not cover_found and 'landscape.jpg' in href:
                    cover_link = urllib.parse.urljoin(film_url, href)
                    cover_found = True
                elif not subtitle_found and href.endswith('.es.srt'):
                    subtitle_link = urllib.parse.urljoin(film_url, href)
                    subtitle_found = True
                elif video_ext_regex.match(href):
                    full_url = urllib.parse.urljoin(film_url, href)
                    video_links.append(full_url)
                elif nfo_ext_regex.match(href):
                    nfo_link = urllib.parse.urljoin(film_url, href)
                    info = extract_xml_data(nfo_link)
                    info["Source"] = video_links
                    nfo_found = True
                    if cover_link:
                        info["Cover"] = cover_link
                    if subtitle_link:
                        info["Subtitle"] = subtitle_link
                    break

        return info

    except Exception as e:
        return {"Error": f"Error getting the media information: {e}"}