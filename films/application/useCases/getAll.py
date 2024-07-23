# Imports
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.decorators import api_view, permission_classes
from films.domain_films.models import Film
from films.application.serializers.films_json import FilmSerializer
from rest_framework.permissions import IsAuthenticated

'''Function to get all films to the DB'''
@api_view(['GET'])
def get_all_films(request):
    try:
        films = Film.objects.all()
        films_json = FilmSerializer(films, many= True).data

        return Response(films_json, status=HTTP_200_OK)

    except Exception as e:
        return ({'Message': 'Something went wrong :( '}, e)