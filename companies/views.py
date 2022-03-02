from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page

from .forms import *
from .models import *
from itgomel.settings import DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL, YANDEX_API_KEY


menu = [
    {'title': 'Главная', 'url_name': 'index'},
    {'title': 'Карта', 'url_name': 'map'},
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
]


# @cache_page(60)
def index(request):
    companies = Company.objects.filter(is_visible=True).distinct()

    paginator = Paginator(companies, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'background': 'index-bg.jpg',
        'companies': companies,
        'menu': menu,
        'page_obj': page_obj,
        'title': 'IT-компании в Гомеле',
    }
    return render(request, 'companies/index.html', context=context)


# @cache_page(60)
def chart(request):
    companies = Company.objects.filter(is_visible=True)

    placemarks_data_list = []

    for company in companies:
        adresses = company.adress_set.all()
        for i in range(len(adresses)):
            placemarks_data = {
                'latitude': float(str(adresses[i]).split('|')[1].split(',')[0]) if str(adresses[i]).split('|')[
                                                                                       1] != 'None' else None,
                'longitude': float(str(adresses[i]).split('|')[1].split(',')[1]) if str(adresses[i]).split('|')[
                                                                                        1] != 'None' else None,
                'iconContent': str(company),
                'hintContent': str(adresses[i]).split('|')[0],
            }
            placemarks_data_list.append(placemarks_data)

    context = {
        'background': 'map-bg.jpg',
        'placemarks_data_list': placemarks_data_list,
        'menu': menu,
        'title': 'Карта IT-компаний',
        'YANDEX_API_KEY': YANDEX_API_KEY,
    }
    return render(request, 'companies/map.html', context=context)


# @cache_page(60)
def about(request):
    context = {
        'background': 'about-bg.jpg',
        'menu': menu,
        'title': 'Описание сайта',
    }
    return render(request, 'companies/about.html', context=context)


# @cache_page(60)
def contact(request):
    form = ContactForm()
    msg_sent = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg_sent = True

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(name,
                      f'{message}\n\n{email}',
                      DEFAULT_FROM_EMAIL,
                      RECIPIENTS_EMAIL,
                      fail_silently=False
                      )

            form = ContactForm()
    else:
        form = ContactForm()

    context = {
        'background': 'contact-bg.jpg',
        'menu': menu,
        'form': form,
        'msg_sent': msg_sent,
        'title': 'Связь с автором',
    }

    return render(request, 'companies/contact.html', context=context)


# @cache_page(60)
def show_company(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    adresses = company.adress_set.all()

    placemarks_data_list = []

    for i in range(len(adresses)):
        placemarks_data = {
            'latitude': float(str(adresses[i]).split('|')[1].split(',')[0]) if str(adresses[i]).split('|')[
                                                                                   1] != 'None' else None,
            'longitude': float(str(adresses[i]).split('|')[1].split(',')[1]) if str(adresses[i]).split('|')[
                                                                                    1] != 'None' else None,
            'iconContent': str(company),
            'hintContent': str(adresses[i]).split('|')[0],
        }
        placemarks_data_list.append(placemarks_data)

    context = {
        'background': 'index-bg.jpg',
        'placemarks_data_list': placemarks_data_list,
        'company': company,
        'menu': menu,
        'name': company.name,
        'title': company,
        'adresses': [str(adress).split('|')[0] for adress in adresses],
        'YANDEX_API_KEY': YANDEX_API_KEY,
    }

    return render(request, 'companies/company.html', context=context)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
