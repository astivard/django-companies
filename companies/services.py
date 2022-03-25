from django.core.mail import send_mail

from itgomel.settings import RECIPIENTS_EMAIL, DEFAULT_FROM_EMAIL


def create_placemark_data_dict(address, company_name) -> dict:
    placemark_data_dict = {
        'latitude': float(address[3].split(',')[0]),
        'longitude': float(address[3].split(',')[1]),
        'iconContent': company_name,
        'hintContent': address[2],
    }
    return placemark_data_dict


def create_placemarks_data_list(company) -> list:
    addresses = company.address_set.all().values_list()
    company_name = company.name
    placemarks_data_list = [create_placemark_data_dict(address, company_name) for address in addresses]
    return placemarks_data_list


def create_placemarks_data_list_for_all_companies(companies) -> list:
    placemarks_data_list = []
    for company in companies:
        addresses = company.address_set.all().values_list()
        for address in addresses:
            placemark_data_dict = create_placemark_data_dict(address, str(company))
            placemarks_data_list.append(placemark_data_dict)
    return placemarks_data_list


def send_email(self):
    name = self.cleaned_data['name']
    email = self.cleaned_data['email']
    message = self.cleaned_data['message']

    send_mail(subject=name,
              message=f'{message}\n\n\n\n'
                      f'------------------'
                      f'------------------'
                      f'------------------'
                      f'\nEmail: {email}',
              from_email=DEFAULT_FROM_EMAIL,
              recipient_list=RECIPIENTS_EMAIL,
              fail_silently=False,
              )
