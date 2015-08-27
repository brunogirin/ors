import django
import rev2
import json
import api.models
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from api.models import HouseCode, INVALID_HOUSE_CODE_MSG, HOUSE_CODE_NOT_FOUND_MSG
from api.models import Debug
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

TIMEOUT_STATUS = 301
INVALID_INPUT_STATUS = 300
VALID_LED_COLOURS = range(4)
VALID_LED_STATES = range(4)
VALID_LED_REPEAT_INTERVALS = range(30, 630, 30)
INVALID_LED_COLOUR_MSG = 'Invalid input for "colour". Received: {}, expected ' + str(VALID_LED_COLOURS)
INVALID_LED_STATE_MSG = 'Invalid input for "state". Received: {}, expected ' + str(VALID_LED_STATES)
INVALID_LED_REPEAT_INTERVAL_MSG = 'Invalid input for "repeat-interval". Received: {}, expected ' + str(VALID_LED_REPEAT_INTERVALS)
MISSING_LED_COLOUR_MSG = 'Missing input for "colour"'
MISSING_LED_STATE_MSG = 'Missing input for "state"'
MISSING_LED_REPEAT_INTERVAL_MSG = 'Missing input for "repeat-interval"'

def status_view(request, house_code):
    response = {'status': 200, 'content': None}
    errors = []

    try:
        house_code = HouseCode.objects.get(code=house_code)
    except HouseCode.DoesNotExist:
        response['status'] = INVALID_INPUT_STATUS
        response['errors'] = [HOUSE_CODE_NOT_FOUND_MSG.format(house_code)]
        return JsonResponse(response)

    response['content'] = house_code.to_dict()
    
    return JsonResponse(response)

@csrf_exempt
def debug_view(request, house_code):
    response = {'status': 200, 'content': None}
    try:
        house_code = HouseCode.objects.get(code=house_code)
        house_code.debug()
    except ObjectDoesNotExist:
        response['status'] = INVALID_INPUT_STATUS
        response['errors'] = [HOUSE_CODE_NOT_FOUND_MSG.format(house_code)]
    return JsonResponse(response)

def api_documentation(request):
    return render(request, 'api/api_documentation.html', {'list': []})

@csrf_exempt
def house_codes(request):
    if request.method == "GET":
        house_codes = [house_code.code for house_code in HouseCode.objects.all()]
        return HttpResponse(json.dumps({"content": house_codes, "status": 200}), content_type="application/json")
    else:
        # get unique house codes
        if request.META['CONTENT_TYPE'] == 'application/json':
            house_code_strings = json.loads(request.body)['house-codes']
        else:
            house_code_strings = [hc.strip() for hc in request.POST['house-codes'].split(',')]
        warnings = []
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

        # validate house codes and verifty they exist
        house_codes = []
        errors = []
        for house_code_str in unique_house_code_strings:
            try:
                house_code = api.models.HouseCode(code=house_code_str)
                rev2.rev2_interface.update_status(house_code=house_code)
                house_codes.append(house_code)
            except ValidationError as e:
                errors.extend(e.message_dict['code'])

        # if they are all valid and exist then delete the old ones and save the new ones
        if len(errors) == 0:
            api.models.HouseCode.objects.all().delete()
            for house_code in house_codes:
                house_code.save()
            rev2.rev2_interface.restart_bg_poller(house_codes=house_codes)
        else:
            response = {'status': INVALID_INPUT_STATUS, 'content': [], 'errors': errors}
            return JsonResponse(response)
            
        response = {}
        response["content"] = [hc.code for hc in house_codes]
        response["status"] = 200
        if len(warnings) >= 1:
            response["warnings"] = warnings

        return JsonResponse(response)

@csrf_exempt
def valve_view_redirect(request):
    house_code = request.POST['house_code']
    return valve_view(request, house_code)

@csrf_exempt
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
        open_input = data['open']
        open_input = int(open_input)
        if open_input < 0 or open_input > 100:
            raise ValueError()
        rev2.rev2_interface.open_valve(house_code=house_code, rad_open_percent=open_input)
    except ValueError:
        errors.append('Invalid input for parameter: open. Received: {}, expected: 0-100'.format(open_input))
        response['status'] = INVALID_INPUT_STATUS
    except MultiValueDictKeyError:
        errors.append('Required input parameter: open')
        response['status'] = INVALID_INPUT_STATUS

    if len(errors):
        response['errors'] = errors

    response = json.dumps(response)
    return HttpResponse(response, content_type='application/json')

@csrf_exempt
def led_view(request, house_code):
    response = {'status': 200, 'content': None}
    errors = []

    try:
        house_code = HouseCode.objects.get(code=house_code)
    except ObjectDoesNotExist:
        response['status'] = INVALID_INPUT_STATUS
        response['errors'] = [HOUSE_CODE_NOT_FOUND_MSG.format(house_code)]
        return JsonResponse(response)

    # colour
    try:
        colour = request.POST['colour']
        colour = int(colour)
        if colour not in VALID_LED_COLOURS:
            raise ValidationError('')
    except (ValidationError, ValueError) as e:
        response['status'] = INVALID_INPUT_STATUS
        errors.append(INVALID_LED_COLOUR_MSG.format(colour))
    except MultiValueDictKeyError:
        response['status'] = INVALID_INPUT_STATUS
        errors.append(MISSING_LED_COLOUR_MSG)

    # state
    try:
        state = request.POST['state']
        state = int(state)
        if state not in VALID_LED_STATES:
            raise ValidationError('')
    except (ValidationError, ValueError) as e:
        response['status'] = INVALID_INPUT_STATUS
        errors.append(INVALID_LED_STATE_MSG.format(state))
    except MultiValueDictKeyError:
        response['status'] = INVALID_INPUT_STATUS
        errors.append(MISSING_LED_STATE_MSG)
        
    # repeat_interval
    try:
        repeat_interval = request.POST['repeat-interval']
        repeat_interval = int(repeat_interval)
        if repeat_interval not in VALID_LED_REPEAT_INTERVALS:
            raise ValidationError('')
    except (ValidationError, ValueError) as e:
        response['status'] = INVALID_INPUT_STATUS
        errors.append(INVALID_LED_REPEAT_INTERVAL_MSG.format(repeat_interval))
    except MultiValueDictKeyError:
        response['status'] = INVALID_INPUT_STATUS
        errors.append(MISSING_LED_REPEAT_INTERVAL_MSG)

    if len(errors):
        response['errors'] = errors
    else:
        rev2.rev2_interface.set_led_settings(house_code=house_code, colour=colour, state=state, repeat_interval=repeat_interval)
        
    return JsonResponse(response)

