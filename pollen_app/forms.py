from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm

from pollen_app.models import FLOWER, SEX
from user.models import CustomUser


class addPlantForm(forms.Form):
    nepenthes = forms.CharField(max_length=500, required=True)
    flower_status = forms.ChoiceField(choices=FLOWER.choices, widget=forms.RadioSelect, required=True)
    sex = forms.ChoiceField(choices=SEX.choices, widget=forms.RadioSelect, required=True)
    image = forms.ImageField(required=True)


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    password2 = None

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:

            # Method inherited from BaseForm
            self.add_error('password1', error)
        return password1
