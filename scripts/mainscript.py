import datetime
import time
import urllib.parse
import requests
from bs4 import BeautifulSoup
from scriptfilm import get_film_data

from sqlalchemy import create_engine, Column, Integer, Float, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

Base = declarative_base()

class Film(Base):
    __tablename__ = 'film'
    id = Column(Integer, primary_key=True)
    source = Column(String)
    title = Column(String)
    director = Column(String)
    sinopsis = Column(Text)
    year = Column(Integer)
    rating = Column(Float)
    genre = Column(String)
    country = Column(String)
    studio = Column(String)

engine = create_engine('sqlite:///db.sqlite3')
Base.metadata.create_all(engine)  # Asegura que todas las tablas estén creadas.
Session = sessionmaker(bind=engine)
session = Session()

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

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


def main():
    base_url = "https://visuales.uclv.cu/Peliculas/Extranjeras/"
    current_year = datetime.datetime.now().year

    for year in range(2000, current_year + 1):
        try:
            movie_folders = get_movie_folders(base_url, year)
            for movie_folder in movie_folders:
                if not movie_folder:
                    print("Empty Folder")
                    continue

                time.sleep(2)
                info_movies = get_film_data(movie_folder)
                if "Error" in info_movies:
                    print(info_movies["Error"])
                    continue
                source = info_movies.get("Source")
                
                film = Film(
                    source=source[0],
                    title=info_movies.get("Title", "Unknown Title"),
                    director=info_movies.get("Director", "Unknown Director"),
                    sinopsis=info_movies.get("Sinopsis", ""),
                    year=info_movies.get("Year", 0),
                    rating=float(info_movies.get("Rating", 0)),
                    genre=info_movies.get("Genre", "Unknown Genre"),
                    country=info_movies.get("Country", "Unknown Country"),
                    studio=info_movies.get("Studio", "Unknown Studio"),
                )
                Session = sessionmaker(bind=engine)
                session = Session()
                session.add(film)
                session.commit()
                session.close()
                print("Success")

        except Exception as e:
            session.rollback()
            print(f"Failed: {e}")

if __name__ == "__main__":
    main()