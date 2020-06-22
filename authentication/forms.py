from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login

class SignUpForm(UserCreationForm):

    email = forms.EmailField(max_length=254, help_text='Required')

    # uncomment it before pushing

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Email is already registered")
    #     return email

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password1', 'password2',)
class LoginForm(forms.Form):

    username = forms.CharField(max_length=256)
    password = forms.CharField(max_length=256,widget=forms.PasswordInput())

    def verify_credentials_and_login_user(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return True
        else:
            return False
