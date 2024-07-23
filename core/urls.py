
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from films.infraestructure import routes as films_routes


urlpatterns = [
    path('admin/', admin.site.urls),
    path('films/', include(films_routes)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
