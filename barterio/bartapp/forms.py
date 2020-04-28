from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Offer, OfferImage

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nazwa użytkownika'
        self.fields['email'].label = 'Adres e-mail'
        self.fields['password'].label = 'Hasło'
        self.fields['password2'].label = 'Powtórz hasło'

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('date_of_birth', 'mobile', 'company_name', 'company_description', 'company_short_description', 'company_account', 'localisation', 'transfer_data')
    
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].label = 'Data urodzenia'
        self.fields['mobile'].label = 'Telefon'
        self.fields['company_name'].label = 'Nazwa firmy (opcjonalnie)'
        self.fields['company_description'].label = 'Opis działalności (opcjonalnie)'
        self.fields['company_short_description'].label = 'Krótki opis działalności (będzie widoczny w każdym ogłoszeniu, opcjonalne)'
        self.fields['company_account'].label = 'Numer konta firmy (opcjonalnie)'
        self.fields['localisation'].label = 'Lokalizacja'
        self.fields['transfer_data'].label = 'Dane do przelewu (opcjonalnie)'


class OfferCreateForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('title', 'category', 'description', 'estimated_value', 'transfer', 'localisation')
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Tytuł'
        self.fields['category'].label = 'Kategoria'
        self.fields['description'].label = 'Opis'
        self.fields['estimated_value'].label = 'Szacowana wartość w PLN'
        self.fields['transfer'].label = 'Forma płatności'
        self.fields['localisation'].label = 'Lokalizacja'

class AddOfferImageForm(forms.Form):
    image = forms.ImageField(label='Obraz')
