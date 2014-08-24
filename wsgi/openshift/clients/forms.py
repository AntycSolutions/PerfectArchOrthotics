from django import forms
from clients.models import Client, Dependent, Insurance

class ClientForm(forms.ModelForm):

    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICES = ((MALE, 'M'),
                      (FEMALE, 'F'))

    firstName = forms.CharField(max_length=128, help_text="Client first name")
    lastName = forms.CharField(max_length=128, help_text="Client last name")
    address = forms.CharField(max_length=128, help_text="Client address")
    city = forms.CharField(max_length=128, help_text="Client edmonton")
    postalCode = forms.CharField(max_length=6, help_text="Client postal code (no spaces)")
    phoneNumber = forms.CharField(max_length=14, help_text="Client home phone")
    cellNumber = forms.CharField(max_length=14, help_text="Client cell phone")
    email = forms.CharField(max_length=254, help_text="Client email")
    birthdate = forms.DateField(help_text="Client birthdate")
    gender = forms.ChoiceField(choices=GENDER_CHOICES, help_text="Gender")
    employer = forms.CharField(max_length=128, help_text="Client employer")

    class Meta:
        model = Client

        fields = ('firstName', 'lastName', 'address', 'city', 'postalCode', 'phoneNumber', 'cellNumber', 'email', 'birthdate', 'gender', 'employer')
