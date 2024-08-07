from django.core.management.base import BaseCommand
import datetime
import time
import urllib.parse
import requests
from bs4 import BeautifulSoup
from films.domain_films.models import Film
from scripts.scriptfilm import get_film_data
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from decouple import Config, Csv, RepositoryEnv

config = Config(RepositoryEnv('.env'))

def get_movie_folders(base_url, year):
    year_url = f"{base_url}{year}/"
    try:
        req = requests.get(year_url)
        if req.status_code == 200:
            html = BeautifulSoup(req.text, "html.parser")
            links = html.find_all('a')
            ignore_texts = ["Name", "Last Modified", "Size", "Description", "Parent Directory"]
            movie_folders = [urllib.parse.urljoin(year_url, link.get('href')) for link in links if link.text.strip() not in ignore_texts and '/' in link.get('href')]
            return movie_folders
        else:
            return []
    except Exception as e:
        print(f"Error accessing {year_url}: {e}")
        return []

class Command(BaseCommand):
    help = 'Fill the Film table with data'

    def handle(self, *args, **kwargs):
        base_url = config('POINT', cast=Csv())
        current_year = datetime.datetime.now().year

        try:
            for year in range(2000, current_year + 1):
                movie_folders = get_movie_folders(base_url, year)
                for movie_folder in movie_folders:
                    if not movie_folder:
                        self.stdout.write("Empty Folder")
                        continue

                    time.sleep(3)
                    info_movies = get_film_data(movie_folder)
                    if "Error" in info_movies:
                        self.stdout.write(info_movies["Error"])
                        continue
                    
                    source = info_movies['Source'][0] if 'Source' in info_movies and info_movies['Source'] else "Unknown Source"
                    
                    film = Film(
                        source=source,
                        title=info_movies.get("Title", "Unknown Title"),
                        director=info_movies.get("Director", "Unknown Director"),
                        sinopsis=info_movies.get("Sinopsis", ""),
                        year=info_movies.get("Year", 0),
                        rating=float(info_movies.get("Rating", 0)),
                        genre=info_movies.get("Genre", "Unknown Genre"),
                        country=info_movies.get("Country", "Unknown Country"),
                        studio=info_movies.get("Studio", "Unknown Studio"),
                        subtitle=info_movies.get("Subtitle", "Unknown Subtitles"),
                    )
                    film.save()

                    cover_url = info_movies.get("Cover", None)
                    if cover_url and cover_url != "Unknown Cover":
                        try:
                            response = requests.get(cover_url)
                            if response.status_code == 200:
                                film.cover.save(f"{film.title}_cover.jpg", ContentFile(response.content), save=True)
                        except Exception as e:
                            print(f"Error al descargar la imagen de la portada: {e}")

                    print("Saved Successfully :)")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed: {e}"))

if __name__ == "__main__":
    command = Command()
    command.handle()