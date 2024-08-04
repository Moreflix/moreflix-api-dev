# Imports
from django.urls import path
from films.application.useCases.getAll import get_all_films
from films.application.useCases.insert import insertar


urlpatterns = [
    path('all/', get_all_films, name='get_all_films'),
    path('insert/', insertar, name='insert'),
]