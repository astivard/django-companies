from django.contrib import admin
from django.urls import include, path

from companies import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('companies.urls')),
]

handler404 = views.page_not_found
handler500 = views.server_error
