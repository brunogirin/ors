import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from api.models import HouseCode, INVALID_HOUSE_CODE_MSG, HOUSE_CODE_NOT_FOUND_MSG
from api.models import Debug

# Create your views here.

INVALID_INPUT_STATUS = 300
VALID_LED_COLOURS = range(4)
VALID_LED_STATES = range(4)
VALID_LED_REPEAT_INTERVALS = range(30, 601)
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
        


    # # flash
    # try:
    #     led.flash = int(request.POST['flash'])
    #     if led.flash not in VALID_FLASH:
    #         raise ValueError()
    # except MultiValueDictKeyError:
    #     errors.append('Required input parameter: flash')
    #     response['status'] = INVALID_INPUT_STATUS
    # except ValueError:
    #     errors.append('Invalid input for parameter: flash. Received: {}, expected: {}'.format(request.POST['flash'], VALID_FLASH))
    #     response['status'] = INVALID_INPUT_STATUS

    # if len(errors) == 0:
    #     led.save()
    # else:
    #     response['errors'] = errors

    if len(errors):
        response['errors'] = errors

    return JsonResponse(response)

def debug_view(request, house_code):
    response = {'status': 200, 'content': None}
    try:
        house_code = HouseCode.objects.get(code="house_code")
    except ObjectDoesNotExist:
        response['status'] = INVALID_INPUT_STATUS
        response['errors'] = [HOUSE_CODE_NOT_FOUND_MSG.format(house_code)]
        # debug = Debug.objects.first()
    # if debug == None:    
    #     debug = Debug.objects.create(state="off")
    # if request.method == "POST":
    #     try:
    #         state = request.POST['state']
    #         if state not in ['on', 'off']:
    #             response['errors'] = ['Invalid input for parameter: state. Received: {}, expected: on/off'.format(state)]
    #             response['status'] = INVALID_INPUT_STATUS
    #         else:
    #             debug.state = state
    #             debug.save()
    #     except MultiValueDictKeyError:
    #         response['errors'] = ['Required input parameter: state']
    #         response['status'] = INVALID_INPUT_STATUS
    # else:
    #     response['content'] = debug.state
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

    if len(errors):
        response['errors'] = errors
    response = json.dumps(response)
    return HttpResponse(response, content_type='application/json')
