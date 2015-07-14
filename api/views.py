import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from ors.models import HouseCode
# Create your views here.

INVALID_INPUT_STATUS = 300

def api_documentation(request):
    return render(request, 'api/api_documentation.html', {'list': []})

def house_codes(request):
    house_codes = [house_code.code for house_code in HouseCode.objects.all()]
    if request.method == "GET":
        return HttpResponse(json.dumps({"content": house_codes, "status": 200}), content_type="application/json")
    else:
        HouseCode.objects.all().delete()
        house_codes = request.POST['house-codes'].split('\r\n')
        warnings = []
        for house_code in house_codes:
            house_code = HouseCode(code=house_code)
            try:
                house_code.full_clean()
                house_code.save()
            except ValidationError as e:
                if dict(e)['code'] == ['This field cannot be blank.']:
                    if 'ignored empty house code(s)' not in warnings:
                        warnings.append('ignored empty house code(s)')
                else:
                    warnings.append('ignored duplicate: {}'.format(house_code.code))
        house_codes = [house_code.code for house_code in HouseCode.objects.all()]
        response = {}
        response["content"] = house_codes
        response["status"] = 200
        if len(warnings) >= 1:
            response["warnings"] = warnings
        return HttpResponse(json.dumps(response), content_type="application/json")

def valve_view(request):
    data = request.POST
    errors = []
    response = {'status': 200, 'content': None}
    min_temp = None

    try:
        open_input = data['open_input']
        open_input = int(open_input)
        if open_input < 0 or open_input > 100:
            raise ValueError()
    except ValueError:
        errors.append('Invalid input for parameter: open_input. Received: {}, expected: 0-100'.format(open_input))
        response['status'] = 300
    except MultiValueDictKeyError:
        errors.append('Required input parameter: open_input')
        response['status'] = 300

    try:
        min_temp = data['min_temp']
        min_temp = int(min_temp)
        if min_temp < 7 or min_temp > 28:
            raise ValueError()
    except ValueError:
        errors.append('Invalid input for parameter: min_temp. Received: {}, expected: 7-28'.format(min_temp))
        response['status'] = 300
    except MultiValueDictKeyError:
        errors.append('Required input parameter: min_temp')
        response['status'] = 300
    
    try:
        max_temp = data['max_temp']
        max_temp = int(max_temp)
        if max_temp < 7 or max_temp > 28:
            raise ValueError()
    except ValueError:
        errors.append('Invalid input for parameter: max_temp. Received: {}, expected: 7-28'.format(max_temp))
        response['status'] = 300
    except MultiValueDictKeyError:
        errors.append('Required input parameter: max_temp')
        response['status'] = 300

    try:
        min_temp = int(data['min_temp'])
        max_temp = int(data['max_temp'])
        if max_temp <= min_temp:
            errors.append("Invalid input for parameter: max_temp. max_temp ({}) must be greater than min_temp ({})".format(max_temp, min_temp))
            response['status'] = 300
    except ValueError:
        pass
    except MultiValueDictKeyError:
        pass

    if len(errors):
        response['errors'] = errors
    response = json.dumps(response)
    return HttpResponse(response, content_type='application/json')
