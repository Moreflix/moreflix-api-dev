# Imports
from django.urls import path
from films.application.useCases.getAll import get_all_films


urlpatterns = [
    path('all/', get_all_films, name='get_all_films'),  
]