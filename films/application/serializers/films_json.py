# Imports
from rest_framework.serializers import ModelSerializer
from films.domain_films.models import Film

class FilmSerializer(ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'