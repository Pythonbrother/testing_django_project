from django.forms import ModelForm
from .models import Epidemic

class Epidemic_insertion_Form(ModelForm):
    class Meta:
        model = Epidemic
        fields = ['name', 'symptoms','topic']
        labels = {
            'name': "Epidemic Name",
            'symptoms': "Symptoms",
        }