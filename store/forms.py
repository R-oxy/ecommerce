from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.http import HttpRequest


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    @method_decorator(csrf_protect)
    def __init__(self, request: HttpRequest, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter username...'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password...'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password...'})
