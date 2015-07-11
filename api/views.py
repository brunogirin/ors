import json
from django.shortcuts import render
from django.http import HttpResponse
from ors.models import HouseCode
# Create your views here.

def api_documentation(request):
    return render(request, 'api/api_documentation.html', {'list': []})

def house_codes(request):
    house_codes = [house_code.code for house_code in HouseCode.objects.all()]
    return HttpResponse(json.dumps({"content": house_codes}), content_type="application/json")
