from django.db import models
from django.db.models.functions import Lower
from django.urls import reverse


class Company(models.Model):
    name = models.CharField(verbose_name='Компания', max_length=100)
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True, db_index=True)
    content = models.TextField(verbose_name='Описание', blank=True)
    logo_url = models.TextField(verbose_name='URL логотипа', blank=True)
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

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        ordering = ['adress_text']


class Resource(models.Model):
    company = models.ForeignKey(Company, verbose_name='Компания', on_delete=models.CASCADE)
    resource = models.CharField(verbose_name='Ресурс', max_length=255)
    resource_url = models.CharField(verbose_name='Ссылка', max_length=255)

    def __str__(self):
        return self.resource + '|' + self.resource_url

    class Meta:
        verbose_name = 'Ресурс'
        verbose_name_plural = 'Ресурсы'
        ordering = ['resource']
