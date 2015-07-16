import api.views
from django.core.exceptions import ValidationError
from api.views import INVALID_INPUT_STATUS
from django.http import JsonResponse
from django.shortcuts import render
from api.forms import ValveForm
from api.models import HouseCode, HOUSE_CODE_NOT_FOUND_MSG

def home(request):
    return render(request, 'ors/home.html', {'valve_form': ValveForm()})

def led_view(request):
    response = {'status': 200, 'content': None}
    house_code = request.POST['house-code']
    return api.views.led_view(request, house_code)
