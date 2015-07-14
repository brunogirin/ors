import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
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
    return HttpResponse(json.dumps({'status': 200, 'content': None}), content_type='application/json')
