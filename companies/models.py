from django.db import models
from django.db.models.functions import Lower
from django.urls import reverse

from geopy.geocoders import Nominatim


class Company(models.Model):
    name = models.CharField(verbose_name='Компания', max_length=100)
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True, db_index=True)
    content = models.TextField(verbose_name='Описание', blank=True)
    logo_url = models.CharField(verbose_name='URL логотипа', max_length=100, blank=True)
    is_visible = models.BooleanField(verbose_name='Отображается?', default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('company', kwargs={'company_slug': self.slug})

    class Meta:
        verbose_name = 'IT-компании Гомеля'
        verbose_name_plural = 'IT-компании Гомеля'
        ordering = [Lower('name'), 'id']


class Adress(models.Model):
    company = models.ForeignKey(Company, verbose_name='Компания', on_delete=models.CASCADE)
    adress_text = models.CharField(verbose_name='Адрес', max_length=255)
    adress_coords = models.CharField(verbose_name='Координаты адреса', max_length=255, blank=True)

    def __str__(self):
        return self.adress_text + '|' + self.adress_coords

    def get_adress_coords(self):
        geolocator = Nominatim(user_agent='-')
        try:
            location = geolocator.geocode(self.adress_text)
            adress_coords = f'{location.latitude},{location.longitude}'
        except AttributeError:
            adress_coords = 'None'

        return adress_coords

    def save(self, *args, **kwargs):
        if not self.adress_coords:
            self.adress_coords = self.get_adress_coords()
        super(Adress, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        ordering = ['adress_text']
