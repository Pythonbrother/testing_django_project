from django.shortcuts import render, redirect
from .forms import Custom_UserCreation_Form

def signup_view(request):
    if request.method == 'GET':
        form = Custom_UserCreation_Form()
        return render(request, 'signup.html', {'form': form})
    else:
        form = Custom_UserCreation_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            errors = list(form.errors.values())
            return render(request, 'signup.html', {'form': form,'errors':errors})
