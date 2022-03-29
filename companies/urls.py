from django.urls import path
from django.views.decorators.cache import cache_page

from .views import CompanyListView, AboutPageView, MapPageView, \
    ContactPageView, SuccesPageView, CompanyDetailView, CompanySearchView


urlpatterns = [
    # path('', cache_page(60)(CompanyListView.as_view()), name='index'),
    path('', CompanyListView.as_view(), name='index'),
    path('search/', CompanySearchView.as_view(), name='search'),
    path('about/', cache_page(60)(AboutPageView.as_view()), name='about'),
    path('map/', cache_page(60)(MapPageView.as_view()), name='map'),
    path('contact/', cache_page(60)(ContactPageView.as_view()), name='contact'),
    path('succes/', SuccesPageView.as_view(), name='succes'),
    path('<slug:company_slug>/', cache_page(60)(CompanyDetailView.as_view()), name='company'),
]
