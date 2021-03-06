from django.contrib import admin

from .models import Company, Address, Resource


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


class ResourcesInline(admin.TabularInline):
    model = Resource
    extra = 1


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_visible')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'conent')
    prepopulated_fields = {'slug': ("name",)}

    inlines = [AddressInline, ResourcesInline]

    fields = ('name', 'slug', 'content', 'logo_url', 'is_visible')


admin.site.register(Company, CompanyAdmin)

admin.site.site_title = 'Администрирование ItGomel'
admin.site.site_header = 'Администрирование ItGomel'
