import django.forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import User_Account

class Custom_UserCreation_Form(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User_Account
        fields = UserCreationForm.Meta.fields + ('username','email','DOB','gender')

class Custom_UserChange_Form(UserChangeForm):
    class Meta:
        model = User_Account
        fields = ['username','password','email']