from django import forms
from clients.models import Client, Dependent, Insurance


class ClientForm(forms.ModelForm):

    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICES = ((MALE, 'Male'),
                      (FEMALE, 'Female'))

    # required
    firstName = forms.CharField(max_length=128, help_text="Client first name")
    lastName = forms.CharField(max_length=128, help_text="Client last name")
    birthdate = forms.CharField(help_text="Client birthdate")

    # not required
    address = forms.CharField(max_length=128, help_text="Client address", required=False)
    city = forms.CharField(max_length=128, help_text="Client city", required=False)
    postalCode = forms.CharField(max_length=6, help_text="Client postal code (no spaces)", required=False)
    phoneNumber = forms.CharField(max_length=14, help_text="Client home phone", required=False)
    cellNumber = forms.CharField(max_length=14, help_text="Client cell phone", required=False)
    email = forms.CharField(max_length=254, help_text="Client email", required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, help_text="Gender", required=False)
    employer = forms.CharField(max_length=128, help_text="Client employer", required=False)
    referredBy = forms.CharField(max_length=128, required=False)
    healthcareNumber = forms.CharField(max_length=20, required=False)

    class Meta:
        model = Client

        fields = ('firstName', 'lastName', 'birthdate', 'address', 'city', 'postalCode', 'phoneNumber',
                  'cellNumber', 'email', 'healthcareNumber', 'gender', 'employer', 'referredBy')


class DependentForm(forms.ModelForm):

    SPOUSE = 'Spouse'
    CHILD = 'Child'
    RELATIONSHIP_CHOICES = ((SPOUSE, 'Spouse'),
                            (CHILD, 'Child'))

    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICES = ((MALE, 'Male'),
                      (FEMALE, 'Female'))

    firstName = forms.CharField(max_length=128, help_text="Dependent first name")
    lastName = forms.CharField(max_length=128, help_text="Dependent last name")
    birthdate = forms.CharField(help_text="Dependent birthdate")
    gender = forms.ChoiceField(choices=GENDER_CHOICES, help_text="Gender", required=False)
    relationship = forms.ChoiceField(choices=RELATIONSHIP_CHOICES, help_text="Relationship", required=False)

    class Meta:
        model = Dependent

        fields = ('firstName', 'lastName', 'birthdate', 'gender', 'relationship')
