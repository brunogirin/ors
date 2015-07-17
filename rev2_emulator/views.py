from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from api.models import HouseCode
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.

def emulator_view(request):
    if request.method == 'POST':
        try:
            temp = request.POST['room-temp']
            house_code = request.POST['house-code']
            house_code = HouseCode.objects.get(code=house_code)
            house_code.temperature_opentrv = temp
            house_code.save()
            return redirect('/')
        except (MultiValueDictKeyError, HouseCode.DoesNotExist):
            return redirect('/rev2-emulator/')
    return render(request, 'rev2_emulator/home.html')
