from .models import Article
from django.forms import ModelForm

class Article_Form(ModelForm):
    class Meta:
        model = Article
        fields = ['name','topic_type','topic','symptoms','causes','photo']