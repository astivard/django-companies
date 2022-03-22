from captcha.fields import ReCaptchaField
from django import forms

from itgomel.settings import RECIPIENTS_EMAIL
from .services import send_mail


class ContactForm(forms.Form):
    name = forms.CharField(label='Ваша компания',
                           max_length=255,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email компании',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Сообщение',
                              widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 60, 'rows': 5}))
    captcha = ReCaptchaField()

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        send_mail(name, email, message, RECIPIENTS_EMAIL)

