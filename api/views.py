import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from api.models import HouseCode, INVALID_HOUSE_CODE_MSG, HOUSE_CODE_NOT_FOUND_MSG
from api.models import Debug, VALID_COLOURS, VALID_FLASH, Led

# Create your views here.

INVALID_INPUT_STATUS = 300

def status_view(request, house_code):
    response = {'status': 200, 'content': None}
    errors = []

    try:
        house_code = HouseCode.objects.get(code=house_code)
    except HouseCode.DoesNotExist:
        response['status'] = INVALID_INPUT_STATUS
        response['errors'] = [HOUSE_CODE_NOT_FOUND_MSG.format(house_code)]
        return JsonResponse(response)

    response['content'] = {
        'house-code': house_code.code,
        'temperature-opentrv': house_code.temperature_opentrv,
        }

#     response['content'] = {'relative-humidity': None, 
#                            'temperature-opentrv': None, 
#                            'temperature-ds18b20': None, 
#                            'window': None, 
#                            'switch': None, 
#                            'last-updated-all': None, 
#                            'last-updated-temperature': None, 
#                            'led': None, 
#                            'synchronising': None, 
#                            'ambient-light': None, 
#                            'house-code': house_code.code
#                            }

    return JsonResponse(response)

def led_view(request, house_code):
    response = {'status': 200, 'content': None}
    errors = []

    try:
        house_code = HouseCode.objects.get(code=house_code)
    except ObjectDoesNotExist:
        response['status'] = INVALID_INPUT_STATUS
        response['errors'] = [HOUSE_CODE_NOT_FOUND_MSG.format(house_code)]
        return JsonResponse(response)

    if Led.objects.count() == 0:
        led = Led.objects.create(colour=0, flash=1)
    else:
        led = Led.objects.first()
    
    # colour
    try:
        led.colour = int(request.POST['colour'])
        if led.colour not in VALID_COLOURS:
            raise ValueError()
    except MultiValueDictKeyError:
        errors.append('Required input parameter: colour')
        response['status'] = INVALID_INPUT_STATUS
    except ValueError:
        errors.append('Invalid input for parameter: colour. Received: {}, expected: {}'.format(request.POST['colour'], VALID_COLOURS))
        response['status'] = INVALID_INPUT_STATUS

    # flash
    try:
        led.flash = int(request.POST['flash'])
        if led.flash not in VALID_FLASH:
            raise ValueError()
    except MultiValueDictKeyError:
        errors.append('Required input parameter: flash')
        response['status'] = INVALID_INPUT_STATUS
    except ValueError:
        errors.append('Invalid input for parameter: flash. Received: {}, expected: {}'.format(request.POST['flash'], VALID_FLASH))
        response['status'] = INVALID_INPUT_STATUS

    if len(errors) == 0:
        led.save()
    else:
        response['errors'] = errors

    return JsonResponse(response)

def debug_view(request):
    response = {'status': 200, 'content': None}
    debug = Debug.objects.first()
    if debug == None:    
        debug = Debug.objects.create(state="off")
    if request.method == "POST":
        try:
            state = request.POST['state']
            if state not in ['on', 'off']:
                response['errors'] = ['Invalid input for parameter: state. Received: {}, expected: on/off'.format(state)]
                response['status'] = INVALID_INPUT_STATUS
            else:
                debug.state = state
                debug.save()
        except MultiValueDictKeyError:
            response['errors'] = ['Required input parameter: state']
            response['status'] = INVALID_INPUT_STATUS
    else:
        response['content'] = debug.state
    return JsonResponse(response)

def api_documentation(request):
    return render(request, 'api/api_documentation.html', {'list': []})

def house_codes(request):
    if request.method == "GET":
        house_codes = [house_code.code for house_code in HouseCode.objects.all()]
        return HttpResponse(json.dumps({"content": house_codes, "status": 200}), content_type="application/json")
    else:
        house_code_strings = [hc.strip() for hc in request.POST['house-codes'].split(',')]
        house_codes = []
        warnings = []
        errors = []

        # check for duplicates
        unique_house_code_strings = []
        duplicates = []
        for house_code in house_code_strings:
            if house_code in unique_house_code_strings:
                duplicates += [house_code]
            else:
                unique_house_code_strings.append(house_code)
        for duplicate in duplicates:
            warnings.append('ignored duplicate: {}'.format(duplicate))
        
        for house_code_str in unique_house_code_strings:
            house_code = HouseCode(code=house_code_str)
            try:
                house_code.full_clean()
                house_codes += [house_code]
            except ValidationError as e:
                if str(e) == "{'code': [u'House code with this Code already exists.']}":
                    house_codes += [house_code]
                else:
                    errors.extend(e.message_dict['code'])

        # return error if there are invalid house codes, empty house codes only return a warning
        if(len(errors)):
            response = {'status': INVALID_INPUT_STATUS, 'content': [], 'errors': errors}
            return JsonResponse(response)

        HouseCode.objects.all().delete()
        for house_code in house_codes:
            house_code.save()

        response = {}
        response["content"] = [hc.code for hc in house_codes]
        response["status"] = 200
        if len(warnings) >= 1:
            response["warnings"] = warnings

        return JsonResponse(response)

def valve_view_redirect(request):
    house_code = request.POST['house_code']
    return valve_view(request, house_code)

def valve_view(request, house_code):

    response = {'status': 200, 'content': None}
    errors = []
    data = request.POST
    min_temp = None

    try:
        house_code = HouseCode.objects.get(code=house_code)
    except HouseCode.DoesNotExist as e:
        response['status'] = INVALID_INPUT_STATUS
        response['errors'] = [HOUSE_CODE_NOT_FOUND_MSG.format(house_code)]
        return JsonResponse(response)

    try:
        open_input = data['open_input']
        open_input = int(open_input)
        if open_input < 0 or open_input > 100:
            raise ValueError()
    except ValueError:
        errors.append('Invalid input for parameter: open_input. Received: {}, expected: 0-100'.format(open_input))
        response['status'] = INVALID_INPUT_STATUS
    except MultiValueDictKeyError:
        errors.append('Required input parameter: open_input')
        response['status'] = INVALID_INPUT_STATUS

    try:
        min_temp = data['min_temp']
        min_temp = int(min_temp)
        if min_temp < 7 or min_temp > 28:
            raise ValueError()
    except ValueError:
        errors.append('Invalid input for parameter: min_temp. Received: {}, expected: 7-28'.format(min_temp))
        response['status'] = INVALID_INPUT_STATUS
    except MultiValueDictKeyError:
        errors.append('Required input parameter: min_temp')
        response['status'] = INVALID_INPUT_STATUS
    
    try:
        max_temp = data['max_temp']
        max_temp = int(max_temp)
        if max_temp < 7 or max_temp > 28:
            raise ValueError()
    except ValueError:
        errors.append('Invalid input for parameter: max_temp. Received: {}, expected: 7-28'.format(max_temp))
        response['status'] = INVALID_INPUT_STATUS
    except MultiValueDictKeyError:
        errors.append('Required input parameter: max_temp')
        response['status'] = INVALID_INPUT_STATUS

    try:
        min_temp = int(data['min_temp'])
        max_temp = int(data['max_temp'])
        if max_temp <= min_temp:
            errors.append("Invalid input for parameter: max_temp. max_temp ({}) must be greater than min_temp ({})".format(max_temp, min_temp))
            response['status'] = INVALID_INPUT_STATUS
    except ValueError:
        pass
    except MultiValueDictKeyError:
        pass

    if len(errors):
        response['errors'] = errors
    response = json.dumps(response)
    return HttpResponse(response, content_type='application/json')
