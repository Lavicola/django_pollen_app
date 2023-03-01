from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from user.models import CustomUser
import re
import requests


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    password2 = None

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1')

    def clean(self, *args, **kwargs):

        cleaned_data = super(UserRegistrationForm, self).clean()
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')

        if email and password:
            if (forbidden_domains(email)):
                raise forms.ValidationError(
                    'Looks like your E-mail is from a trashmail provider, if not please contact the Admin')
            user = CustomUser.objects.filter(email=email).first()
            if user:
                if not user.is_active:
                    raise forms.ValidationError(
                        'Email was not verified')


# check if trash mail or fb
def forbidden_domains(email):
    domain = re.search("@.*", email)
    url = "https://www.block-trashmail.space/api/" + domain.group()
    r = requests.get(url)
    if (r.json()):
        return True
    elif ("fangblatt" in email):
        return True
    return False


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):

        cleaned_data = super(UserLoginForm, self).clean()

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = CustomUser.objects.filter(email=email).first()
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Password Incorrect!')
            if not user.is_active:
                raise forms.ValidationError('You did not verify your email, please do that before you try to log in')
        else:
            raise forms.ValidationError('Password or Email missing!')
