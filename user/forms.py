from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms

from user.models import CustomUser


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


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):

        cleaned_data = super(UserLoginForm,self).clean()

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Password Incorrect!')
            if not user.is_active:
                raise forms.ValidationError('You did not verify your email, please do that before you try to log in')
        else:
            raise forms.ValidationError('Password or Email missing!')

