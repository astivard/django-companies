from django.urls import path

from . import views


urlpatterns = [
    path('', views.CompanyListView.as_view(), name='index'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('map/', views.MapPageView.as_view(), name='map'),
    path('contact/', views.ContactPageView.as_view(), name='contact'),
    path('succes/', views.SuccesPageView.as_view(), name='succes'),
    path('<slug:company_slug>/', views.CompanyDetailView.as_view(), name='company'),
]
