from django import forms
from captcha.fields import ReCaptchaField


class ContactForm(forms.Form):
    name = forms.CharField(label='Ваша компания', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email компании', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Сообщение',
                              widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 60, 'rows': 5}))
    captcha = ReCaptchaField()

