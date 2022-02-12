from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from companies import views
from itgomel import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('companies.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.page_not_found
