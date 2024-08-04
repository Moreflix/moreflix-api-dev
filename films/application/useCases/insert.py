from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from films.domain_films.models import Film
from films.application.serializers.films_json import FilmSerializer


@api_view(['POST'])
def insertar(request):
    data = request.data
    if not data:
        return Response({'Message':'No data yet'},
                        status=HTTP_400_BAD_REQUEST)
    else:
        try:
            movie = Film.objects.create(**data)
            movie.save()
            return Response({'Message':'Movie has saved successfully'},
                            status=HTTP_201_CREATED)
        except Exception as e:
            return Response({'Message':'Movie not saved, something went wrong',
                             'Error Message':f'{e}'},
                            status=HTTP_400_BAD_REQUEST)