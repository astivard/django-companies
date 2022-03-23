from django.core.mail import send_mail

from itgomel.settings import DEFAULT_FROM_EMAIL


def create_placemark_data_dict(address, company_name) -> dict:
    placemark_data_dict = {
        'latitude': float(address[3].split(',')[0]),
        'longitude': float(address[3].split(',')[1]),
        'iconContent': company_name,
        'hintContent': address[2],
    }
    return placemark_data_dict


def create_placemarks_data_list(company) -> list:
    addresses = company.adress_set.all().values_list()
    company_name = company.name
    placemarks_data_list = [create_placemark_data_dict(address, company_name) for address in addresses]
    return placemarks_data_list


def create_placemarks_data_list_for_all_companies(companies) -> list:
    placemarks_data_list = []
    for company in companies:
        addresses = company.adress_set.all().values_list()
        for address in addresses:
            placemark_data_dict = create_placemark_data_dict(address, str(company))
            placemarks_data_list.append(placemark_data_dict)
    return placemarks_data_list


def send_email(name: str, message: str, email: str, recepient_list: list):
    send_mail(name,
              f'{message}\n\n{email}',
              DEFAULT_FROM_EMAIL,
              recepient_list,
              fail_silently=False
              )

