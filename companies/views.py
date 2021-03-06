from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, TemplateView

from .forms import ContactForm
from .models import Company
from .services import create_placemarks_data_list, create_placemarks_data_list_for_all_companies
from .utils import DataMixin, menu


class CompanyListView(DataMixin, ListView):
    """View class for the main page"""
    paginate_by = 5
    model = Company
    template_name = 'companies/index.html'
    context_object_name = 'company'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='IT-компании в Гомеле', background='index-bg.jpg')
        return {**context, **context_def}

    def get_queryset(self):
        return Company.objects.filter(is_visible=True)


class CompanySearchView(DataMixin, ListView):
    """View class for search results"""
    model = Company
    template_name = 'companies/search.html'
    context_object_name = 'company'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Результаты поиска', background='index-bg.jpg')
        return {**context, **context_def}

    def get_queryset(self):
        search_query = self.request.GET.get('q')
        return Company.objects.filter(is_visible=True, name__icontains=search_query), search_query


class MapPageView(DataMixin, ListView):
    """View class for the map page"""
    model = Company
    template_name = "companies/map.html"
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['placemarks_data_list'] = create_placemarks_data_list_for_all_companies(context['company'])
        context_def = self.get_user_context(title='Карта IT-компаний', background='map-bg.jpg')
        return {**context, **context_def}

    def get_queryset(self):
        return Company.objects.filter(is_visible=True)


class AboutPageView(DataMixin, TemplateView):
    """View class for the about page"""
    template_name = "companies/about.html"

    def get_context_data(self, **kwargs):
        return self.get_user_context(title='Описание сайта', background='about-bg.jpg')


class ContactPageView(DataMixin, FormView):
    """View class for the contact page"""
    form_class = ContactForm
    template_name = "companies/contact.html"
    context_object_name = 'company'
    success_url = reverse_lazy('succes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        def_context = self.get_user_context(title='Связь с автором',
                                            background='contact-bg.jpg')
        return {**context, **def_context}

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class SuccesPageView(DataMixin, TemplateView):
    """View class for the succes page after sending email"""
    template_name = "companies/message.html"

    def get_context_data(self, **kwargs):
        return self.get_user_context(title='Сообщение отправлено', background='contact-bg.jpg')


class CompanyDetailView(DataMixin, DetailView):
    """View class for the certain company page"""
    model = Company
    template_name = 'companies/company.html'
    slug_url_kwarg = 'company_slug'
    context_object_name = 'company'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['company'].name
        context['addresses'] = context['company'].address_set.all()
        context['resources'] = context['company'].resource_set.all().values_list()
        context['placemarks_data_list'] = create_placemarks_data_list(context['company'])
        context_def = self.get_user_context(background='index-bg.jpg')
        return {**context, **context_def}


def page_not_found(request, exception):
    return render(request, 'companies/message.html', {'menu': menu,
                                                      'background': 'index-bg.jpg',
                                                      'title': 'Страница не найдена'})


def server_error(request, *args, **argv):
    return render(request, 'companies/message.html', {'menu': menu,
                                                      'background': 'index-bg.jpg',
                                                      'title': 'Ошибка сервера'})
