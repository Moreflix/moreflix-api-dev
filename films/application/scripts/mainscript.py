import datetime
import time
import urllib.parse
import requests
from bs4 import BeautifulSoup
from scriptfilm import get_film_data

def get_movie_folders(base_url, year):
    year_url = f"{base_url}{year}/"
    try:
        req = requests.get(year_url)
        if req.status_code == 200:
            html = BeautifulSoup(req.text, "html.parser")
            links = html.find_all('a')
            # Lista de textos a ignorar
            ignore_texts = ["Name", "Last Modified", "Size", "Description", "Parent Directory"]
            # Filtra los links que no contienen los textos a ignorar
            movie_folders = [urllib.parse.urljoin(year_url, link.get('href')) for link in links if link.text.strip() not in ignore_texts and '/' in link.get('href')]
            return movie_folders
        else:
            return []
    except Exception as e:
        print(f"Error accessing {year_url}: {e}")
        return []


def main():
    base_url = "https://visuales.uclv.cu/Peliculas/Extranjeras/"
    current_year = datetime.datetime.now().year

    for year in range(2000, current_year + 1):
        movie_folders = get_movie_folders(base_url, year)
        for movie_folder in movie_folders:
            time.sleep(2)
            if movie_folder:
                info_movies = get_film_data(movie_folder)
                if info_movies:    
                    for key, value in info_movies.items():
                        print(f"{key}: {value}")
            else:
                return print("Empty Folder")

if __name__ == "__main__":
    main()