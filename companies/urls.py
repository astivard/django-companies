from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('map/', views.chart, name='map'),
    path('contact/', views.contact, name='contact'),
    path('<slug:company_slug>/', views.show_company, name='company'),
]
