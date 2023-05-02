from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from .models import Room, User

# for registration form
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["name", "username", "email", "password1", "password2"]

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__" # can be ["name", "body"]
        exclude=["host", "participants"]

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "name", "username", "email","bio"]