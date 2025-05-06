from django.forms import ModelForm
from .models import Epidemic

class Epidemic_insertion_Form(ModelForm):
    class Meta:
        model = Epidemic
        fields = ['name', 'symptoms', 'prevention_tips', 'managing_tips']
        labels = {
            'name': "Epidemic Name",
            'symptoms': "Symptoms",
            'prevention_tips': "Tips Of Prevention",
            'managing_tips': "Tips of Managing"
        }