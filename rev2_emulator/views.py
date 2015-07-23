from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from api.models import HouseCode
from django.utils.datastructures import MultiValueDictKeyError
from api.views import INVALID_INPUT_STATUS
from api.models import HOUSE_CODE_NOT_FOUND_MSG
# Create your views here.

def emulator_view(request):
    return render(request, 'rev2_emulator/home.html')

def relative_humidity_view(request):
    response = {'status': 200, 'content': None}
    try:
        hc = HouseCode.objects.get(code=request.POST['house-code'])
        hc.relative_humidity = request.POST['relative-humidity']
        try:
            hc.full_clean()
            hc.save()
        except ValidationError as e:
            response['status'] = INVALID_INPUT_STATUS
            response['errors'] = e.message_dict['relative_humidity']
    except HouseCode.DoesNotExist:
        response['status'] = INVALID_INPUT_STATUS
        response['errors'] = [HOUSE_CODE_NOT_FOUND_MSG.format(request.POST['house-code'])]
    return JsonResponse(response)

def temperature_opentrv_view(request):
    response = {'status': 200, 'content': None}
    try:
        hc = HouseCode.objects.get(code=request.POST['house-code'])
        hc.temperature_opentrv = request.POST['temperature-opentrv']
        try:
            hc.full_clean()
            hc.save()
        except ValidationError as e:
            response['status'] = INVALID_INPUT_STATUS
            response['errors'] = e.message_dict['temperature_opentrv']
    except HouseCode.DoesNotExist:
        response['status'] = INVALID_INPUT_STATUS
        response['errors'] = [HOUSE_CODE_NOT_FOUND_MSG.format(request.POST['house-code'])]
    return JsonResponse(response)
        
def temperature_ds18b20_view(request):
    response = {'status': 200, 'content': None}
    try:
        hc = HouseCode.objects.get(code=request.POST['house-code'])
        hc.temperature_ds18b20 = request.POST['temperature-ds18b20']
        try:
            hc.full_clean()
            hc.save()
        except ValidationError as e:
            response['status'] = INVALID_INPUT_STATUS
            response['errors'] = e.message_dict['temperature_ds18b20']
    except HouseCode.DoesNotExist:
        response['status'] = INVALID_INPUT_STATUS
        response['errors'] = [HOUSE_CODE_NOT_FOUND_MSG.format(request.POST['house-code'])]
    return JsonResponse(response)

def window_view(request):
    response = {'status': 200, 'content': None}
    try:
        hc = HouseCode.objects.get(code=request.POST['house-code'])
        hc.window = request.POST['window']
        try:
            hc.full_clean()
            hc.save()
        except ValidationError as e:
            response['status'] = INVALID_INPUT_STATUS
            response['errors'] = e.message_dict['window']
    except HouseCode.DoesNotExist:
        response['status'] = INVALID_INPUT_STATUS
        response['errors'] = [HOUSE_CODE_NOT_FOUND_MSG.format(request.POST['house-code'])]
    return JsonResponse(response)

def switch_view(request):
    response = {'status': 200, 'content': None}
    try:
        hc = HouseCode.objects.get(code=request.POST['house-code'])
        hc.switch = request.POST['switch']
        try:
            hc.full_clean()
            hc.save()
        except ValidationError as e:
            response['status'] = INVALID_INPUT_STATUS
            response['errors'] = e.message_dict['switch']
    except HouseCode.DoesNotExist:
        response['status'] = INVALID_INPUT_STATUS
        response['errors'] = [HOUSE_CODE_NOT_FOUND_MSG.format(request.POST['house-code'])]
    return JsonResponse(response)

def last_updated_all_view(request):
    response = {'status': 200, 'content': None}
    try:
        hc = HouseCode.objects.get(code=request.POST['house-code'])
        hc.last_updated_all = request.POST['last-updated-all']
        try:
            hc.full_clean()
            hc.save()
        except ValidationError as e:
            print e
            response['status'] = INVALID_INPUT_STATUS
            response['errors'] = e.message_dict['last_updated_all']
    except HouseCode.DoesNotExist:
        response['status'] = INVALID_INPUT_STATUS
        response['errors'] = [HOUSE_CODE_NOT_FOUND_MSG.format(request.POST['house-code'])]
    return JsonResponse(response)

def last_updated_temperature_view(request):
    response = {'status': 200, 'content': None}
    try:
        hc = HouseCode.objects.get(code=request.POST['house-code'])
        hc.last_updated_temperature = request.POST['last-updated-temperature']
        try:
            hc.full_clean()
            hc.save()
        except ValidationError as e:
            response['status'] = INVALID_INPUT_STATUS
            response['errors'] = e.message_dict['last_updated_temperature']
    except HouseCode.DoesNotExist:
        response['status'] = INVALID_INPUT_STATUS
        response['errors'] = [HOUSE_CODE_NOT_FOUND_MSG.format(request.POST['house-code'])]
    return JsonResponse(response)

def synchronising_view(request):
    response = {'status': 200, 'content': None}
    try:
        hc = HouseCode.objects.get(code=request.POST['house-code'])
        hc.synchronising = request.POST['synchronising']
        try:
            hc.full_clean()
            hc.save()
        except ValidationError as e:
            response['status'] = INVALID_INPUT_STATUS
            response['errors'] = e.message_dict['synchronising']
    except HouseCode.DoesNotExist:
        response['status'] = INVALID_INPUT_STATUS
        response['errors'] = [HOUSE_CODE_NOT_FOUND_MSG.format(request.POST['house-code'])]
    return JsonResponse(response)

def ambient_light_view(request):
    response = {'status': 200, 'content': None}
    try:
        hc = HouseCode.objects.get(code=request.POST['house-code'])
        hc.ambient_light = request.POST['ambient-light']
        try:
            hc.full_clean()
            hc.save()
        except ValidationError as e:
            response['status'] = INVALID_INPUT_STATUS
            response['errors'] = e.message_dict['ambient_light']
    except HouseCode.DoesNotExist:
        response['status'] = INVALID_INPUT_STATUS
        response['errors'] = [HOUSE_CODE_NOT_FOUND_MSG.format(request.POST['house-code'])]
    return JsonResponse(response)

def get_statuses(request):
    response = {'content': [], 'status': 200}
    for hc in HouseCode.objects.all():
        response['content'] += [hc.to_dict()]
    return JsonResponse(response)
