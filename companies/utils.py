menu = (
    {'title': 'Главная', 'url_name': 'index'},
    {'title': 'Карта', 'url_name': 'map'},
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
)


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context

