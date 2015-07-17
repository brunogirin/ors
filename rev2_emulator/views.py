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

def ds18b20_temperature_view(request):
    hc = HouseCode.objects.get(code=request.POST['house-code'])
    hc.ds18b20_temperature = request.POST['ds18b20-temp']
    hc.save()
    return JsonResponse({'status': 200, 'content': None})

def button_view(request):
    hc = HouseCode.objects.get(code=request.POST['house-code'])
    hc.button = request.POST['button']
    hc.save()
    return JsonResponse({'status': 200, 'content': None})

def led_view(request):
    hc = HouseCode.objects.get(code=request.POST['house-code'])
    hc.led = request.POST['led']
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

def last_updated_view(request):
    hc = HouseCode.objects.get(code=request.POST['house-code'])
    hc.last_updated = request.POST['last-updated']
    hc.save()
    return JsonResponse({'status': 200, 'content': None})

def last_updated_temperatures_view(request):
    hc = HouseCode.objects.get(code=request.POST['house-code'])
    hc.last_updated_temperatures = request.POST['last-updated-temperatures']
    hc.save()
    return JsonResponse({'status': 200, 'content': None})

def get_statuses(request):
    content = []
    for hc in HouseCode.objects.all():
        x = {
            'house-code': hc.code,
            'temperature-opentrv': hc.temperature_opentrv,
            'ds18b20-temperature': hc.ds18b20_temperature,
            'button': hc.button,
            'led': hc.led,
            'synchronising': hc.synchronising,
            'relative-humidity': hc.relative_humidity,
            'window': hc.window,
            'last-updated': hc.last_updated.isoformat() if hc.last_updated else hc.last_updated,
            'last-updated-temperatures': hc.last_updated_temperatures.isoformat() if hc.last_updated_temperatures else None,
            }
        content += [x]
    return JsonResponse({'status': 200, 'content': content})
