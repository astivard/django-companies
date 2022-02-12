from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Company, Adress


class AdressInline(admin.TabularInline):
    model = Adress
    extra = 1


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_html_logo', 'is_visible')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'conent')
    prepopulated_fields = {'slug': ("name",)}

    inlines = [AdressInline]

    fields = ('name', 'slug', 'content', 'logo', 'get_html_logo', 'is_visible')
    readonly_fields = ('get_html_logo', )

    def get_html_logo(self, object):
        if object.logo:
            return mark_safe(f"<img src='{object.logo.url}' width=25>")

    get_html_logo.short_description = "Логотип"


admin.site.register(Company, CompanyAdmin)

admin.site.site_title = 'Администрирование ItGomel'
admin.site.site_header = 'Администрирование ItGomel'
