from django.shortcuts import render

def home(request):
    return render(request, 'ors/home.html')
