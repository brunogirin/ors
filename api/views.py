import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from api.models import HouseCode
from api.models import Debug, VALID_COLOURS, VALID_FLASH, Led
# Create your views here.

INVALID_INPUT_STATUS = 300

def status_view(request):
    return JsonResponse({'status': 200, 'content': {'relative-humidity': 0, 'temperature-opentrv': 0, 'temperature-ds18b20': 0, 'window': 0, 'switch': 0, 'last-updated-all': 0, 'last-updated-temperature': 0, 'led': 0, 'synchronising': 0, 'ambient-light': 0, 'house-code': 0}})

def led_view(request):
    response = {'status': 200, 'content': None}
    errors = []
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
                try:
                    assert(len(house_code.code) ==  5)
                    assert(house_code.code[2] == '-')
                    (hex1, hex2) = house_code.code.split('-')
                    hex1 = int(hex1, 16)
                    hex2 = int(hex2, 16)
                    house_codes += [house_code]
                except (IndexError, AssertionError, ValueError) as e:
                    errors.append('Invalid house-code. Recieved: {}, expected XX-XX where XX are uppercase hex numbers'.format(house_code.code))
            except ValidationError as e:
                if str(e) == "{'code': [u'This field cannot be blank.']}":
                    if 'ignored empty house code(s)' not in warnings:
                        warnings.append('ignored empty house code(s)')
                elif str(e) == "{'code': [u'House code with this Code already exists.']}":
                    house_codes += [house_code]
                else:
                    raise(e)

#         # check if any house codes passed validation
#         if len(house_codes) == 0:
#             errors.append('No valid house codes found')

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
