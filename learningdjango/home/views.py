from django.shortcuts import render
from .forms import RegistrationForm
from django.http import HttpResponseRedirect
from django.template.context_processors import request

def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        
    return render(request, 'pages/register.html', {'form' : form})