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
    content = []
    for hc in HouseCode.objects.all():
        x = {
            'house-code': hc.code,
            'temperature-opentrv': hc.temperature_opentrv,
            'temperature-ds18b20': hc.temperature_ds18b20,
            'switch': hc.switch,
            'synchronising': hc.synchronising,
            'relative-humidity': hc.relative_humidity,
            'window': hc.window,
            'last-updated_all': hc.last_updated_all.isoformat() if hc.last_updated_all else hc.last_updated_all,
            'last-updated-temperature': hc.last_updated_temperature.isoformat() if hc.last_updated_temperature else None,
            }
        content += [x]
    return JsonResponse({'status': 200, 'content': content})
