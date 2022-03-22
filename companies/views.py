from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, TemplateView

from .forms import ContactForm
from .models import Company
from .services import menu, create_placemarks_data_list, create_placemarks_data_list_for_all_companies


class CompanyListView(ListView):
    """View class for the main page"""
    paginate_by = 3
    model = Company
    template_name = 'companies/index.html'
    context_object_name = 'company'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'IT-компании в Гомеле'
        context['background'] = 'index-bg.jpg'
        return context

    def get_queryset(self):
        # return Company.objects.filter(is_visible=True).distinct()
        return Company.objects.filter(is_visible=True)


class MapPageView(ListView):
    """View class for the map page"""
    model = Company
    template_name = "companies/map.html"
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Карта IT-компаний'
        context['background'] = 'map-bg.jpg'
        context['placemarks_data_list'] = create_placemarks_data_list_for_all_companies(context['company'])
        return context

    def get_queryset(self):
        return Company.objects.filter(is_visible=True)


class AboutPageView(TemplateView):
    """View class for the about page"""
    template_name = "companies/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Описание сайта'
        context['background'] = 'about-bg.jpg'
        return context


class ContactPageView(FormView):
    """View class for the contact page"""
    form_class = ContactForm
    template_name = "companies/contact.html"
    context_object_name = 'company'
    success_url = reverse_lazy('contact')
    is_msg_sent = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Связь с автором'
        context['background'] = 'contact-bg.jpg'
        context['is_msg_sent'] = ContactPageView.is_msg_sent
        return context

    def form_valid(self, form):
        form.send_email()
        ContactPageView.is_msg_sent = True
        return super().form_valid(form)


class CompanyDetailView(DetailView):
    """View class for the certain company page"""
    model = Company
    template_name = 'companies/company.html'
    slug_url_kwarg = 'company_slug'
    context_object_name = 'company'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['background'] = 'index-bg.jpg'
        context['title'] = context['company'].name
        context['addresses'] = context['company'].adress_set.all()  # address
        context['resources'] = context['company'].resource_set.all().values_list()
        context['placemarks_data_list'] = create_placemarks_data_list(context['company'])
        return context

    def get_queryset(self):
        return Company.objects.filter(is_visible=True)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
