from django.shortcuts import render

from api.forms import ValveForm

def home(request):
    return render(request, 'ors/home.html', {'valve_form': ValveForm()})
