import json
from django.shortcuts import render
from django.http import HttpResponse
from ors.models import HouseCode
# Create your views here.

def api_documentation(request):
    return render(request, 'api/api_documentation.html', {'list': []})

def house_codes(request):
    house_codes = [house_code.code for house_code in HouseCode.objects.all()]
    if request.method == "POST":
        house_codes = request.POST['house-codes'].split('\r\n')
        for house_code in house_codes:
            HouseCode.objects.create(code=house_code)
        house_codes = [house_code.code for house_code in HouseCode.objects.all()]
    return HttpResponse(json.dumps({"content": house_codes, "status": 200}), content_type="application/json")
