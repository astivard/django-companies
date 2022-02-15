from django.contrib import admin

from .models import Company, Adress


class AdressInline(admin.TabularInline):
    model = Adress
    extra = 1


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_visible')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'conent')
    prepopulated_fields = {'slug': ("name",)}

    inlines = [AdressInline]

    fields = ('name', 'slug', 'content', 'logo_url', 'is_visible')


admin.site.register(Company, CompanyAdmin)

admin.site.site_title = 'Администрирование ItGomel'
admin.site.site_header = 'Администрирование ItGomel'
