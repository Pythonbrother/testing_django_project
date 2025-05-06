from django.shortcuts import render
from django.http import HttpResponse
from .forms import Epidemic_insertion_Form
from .models import Epidemic
import re
def home_view(request):
    if request.method=="GET":
        return render(request, 'home.html')

def epidemic_insertion_view(request):
    if request.method == 'POST':
        form = Epidemic_insertion_Form(request.POST)
        if form.is_valid():
            epidemic_record = form.save(commit=False)
            epidemic_record.creator = request.user.username
            epidemic_record.save()
        return HttpResponse("Epidemic Insertion Success")
    else:
        form = Epidemic_insertion_Form()
    return render(request, 'epidemic_insertion_template.html', {'form':form})

def examine_prevention_tip(request):
    if request.method == 'GET':
        epidemic_record = Epidemic.objects.get(id=1)
        epidemic_prevention_tips = re.sub('#','',epidemic_record.prevention_tips).split("!")
        total_tips = len(epidemic_prevention_tips)
        return render(request, 'examine_prevention_tip.html', {"epidemic":epidemic_record,"tips":epidemic_prevention_tips,'total_tip':total_tips})
    else:
        epidemic_record = Epidemic.objects.get(id=1)
        epidemic_prevention_tips = re.sub('#', '', epidemic_record.prevention_tips).split("!")
        total_tips = len(epidemic_prevention_tips)
        checked_tips = request.POST.getlist("prevention_tips")
        total_checked_tips = len(request.POST.getlist("prevention_tips"))

        prevention_percent = (total_checked_tips/total_tips)*100
        return HttpResponse(f"Hello Success, you get {prevention_percent}")

def examine_managing_tip(request):
    if request.method == 'GET':
        epidemic_record = Epidemic.objects.get(id=1)
        epidemic_managing_tips = re.sub('#','',epidemic_record.managing_tips).split("!")
        total_tips = len(epidemic_managing_tips)
        return render(request, 'examine_managing_tip.html', {"epidemic":epidemic_record,"tips":epidemic_managing_tips,'total_tip':total_tips})
    else:
        epidemic_record = Epidemic.objects.get(id=1)
        epidemic_managing_tips = re.sub('#', '', epidemic_record.managing_tips).split("!")
        total_tips = len(epidemic_managing_tips)
        checked_tips = request.POST.getlist("managing_tips")
        total_checked_tips = len(request.POST.getlist("managing_tips"))

        managing_percent = (total_checked_tips/total_tips)*100
        return HttpResponse(f"Hello Success, you get {managing_percent}")