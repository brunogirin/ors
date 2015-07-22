from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from api.models import HouseCode
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.

def emulator_view(request):
    return render(request, 'rev2_emulator/home.html')

def temperature_opentrv_view(request):
    hc = HouseCode.objects.get(code=request.POST['house-code'])
    hc.temperature_opentrv = request.POST['room-temp']
    hc.save()
    return JsonResponse({'status': 200, 'content': None})

def temperature_ds18b20_view(request):
    hc = HouseCode.objects.get(code=request.POST['house-code'])
    hc.temperature_ds18b20 = request.POST['temperature-ds18b20']
    hc.save()
    return JsonResponse({'status': 200, 'content': None})

def switch_view(request):
    hc = HouseCode.objects.get(code=request.POST['house-code'])
    hc.switch = request.POST['switch']
    hc.save()
    return JsonResponse({'status': 200, 'content': None})

def synchronising_view(request):
    hc = HouseCode.objects.get(code=request.POST['house-code'])
    hc.synchronising = request.POST['synchronising']
    hc.save()
    return JsonResponse({'status': 200, 'content': None})

def relative_humidity_view(request):
    hc = HouseCode.objects.get(code=request.POST['house-code'])
    hc.relative_humidity = request.POST['relative-humidity']
    hc.save()
    return JsonResponse({'status': 200, 'content': None})

def window_view(request):
    hc = HouseCode.objects.get(code=request.POST['house-code'])
    hc.window = request.POST['window']
    hc.save()
    return JsonResponse({'status': 200, 'content': None})

def last_updated_all_view(request):
    hc = HouseCode.objects.get(code=request.POST['house-code'])
    hc.last_updated_all = request.POST['last-updated-all']
    hc.save()
    return JsonResponse({'status': 200, 'content': None})

def last_updated_temperature_view(request):
    hc = HouseCode.objects.get(code=request.POST['house-code'])
    hc.last_updated_temperature = request.POST['last-updated-temperature']
    hc.save()
    return JsonResponse({'status': 200, 'content': None})

def get_statuses(request):
    response = {'content': [], 'status': 200}
    for hc in HouseCode.objects.all():
        response['content'] += [hc.to_dict()]
    return JsonResponse(response)
