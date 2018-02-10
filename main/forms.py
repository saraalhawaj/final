from django import forms 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from main.models import CustomUser

from .models import Myfeed, Reply

class MyfeedForm(forms.ModelForm):
    class Meta:
        model = Myfeed
        fields = [ 'feed', 'book','course', 'major']


class UserSignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'major','course']

        widgets = {
        	'password': forms.PasswordInput(),
        }



class UserLoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput())


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'major' , 'course']

