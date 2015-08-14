import collections
import json
import datetime
import rev2_emulator.views
import api.models
from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpResponse, JsonResponse
from api.models import HouseCode
from api.views import INVALID_INPUT_STATUS
# Create your tests here.

class GetStatusesTest(TestCase):

    def test_url(self):
        found = resolve('/rev2-emulator/get-statuses')
        self.assertEqual(found.func, rev2_emulator.views.get_statuses)

    def test_empty_house_code_database(self):
        response = self.client.get('/rev2-emulator/get-statuses')
        response = json.loads(response.content)
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['content'], [])

    def test_default_house_code_object(self):
        hc = HouseCode.objects.create(code='FA-32')
        response = self.client.get('/rev2-emulator/get-statuses')
        response = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(response.content)
        self.assertEqual([hc.to_dict()], response['content'])

    def test_multiple_house_code_objects(self):
        hc1 = HouseCode.objects.create(code='FA-32')
        hc2 = HouseCode.objects.create(code='EE-EE', temperature_opentrv=23.333)
        response = self.client.get('/rev2-emulator/get-statuses')
        response = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(response.content)
        self.assertEqual([hc1.to_dict(), hc2.to_dict()], response['content'])

class EmulatorViewTest(TestCase):

    def test_url(self):
        found = resolve('/rev2-emulator/')
        self.assertEqual(found.func, rev2_emulator.views.emulator_view)
        
    def test_template(self):
        response = self.client.get('/rev2-emulator/')
        self.assertTemplateUsed(response, 'rev2_emulator/home.html')

class TemperatureOpentrvViewTest(TestCase):

    def test_url(self):
        found = resolve('/rev2-emulator/temperature-opentrv')
        self.assertEqual(found.func, rev2_emulator.views.temperature_opentrv_view)
    
    def test_post_updates(self):
        hc = HouseCode.objects.create(code="FA-32")
        response = self.client.post('/rev2-emulator/temperature-opentrv', data={'house-code': 'FA-32', 'temperature-opentrv': '10.123'})
        hc = HouseCode.objects.all()[0]
        hc = HouseCode.objects.first()
        self.assertEqual(hc.temperature_opentrv, 10.123)

    def test_alphabetical_input(self):
        hc = HouseCode.objects.create(code='FA-32')
        data = {'house-code': hc.code, 'temperature-opentrv': 'asdf'}
        response = self.client.post('/rev2-emulator/temperature-opentrv', data=data)
        response = json.loads(response.content)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(response['errors'], [api.models.INVALID_TEMPERATURE_OPENTRV_MSG.format('asdf')])

    def test_invalid_precision(self):
        hc = HouseCode.objects.create(code='FA-32')
        data = {'house-code': hc.code, 'temperature-opentrv': '12.22223'}
        response = self.client.post('/rev2-emulator/temperature-opentrv', data=data)
        response = json.loads(response.content)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(response['errors'], [api.models.INVALID_TEMPERATURE_OPENTRV_MSG.format('12.22223')])
        
        
class TemperatureDs18b20ViewTest(TestCase):

    def test_url(self):
        found = resolve('/rev2-emulator/temperature-ds18b20')
        self.assertEqual(found.func, rev2_emulator.views.temperature_ds18b20_view)
    
    def test_post_updates(self):
        hc = HouseCode.objects.create(code="FA-32")
        response = self.client.post('/rev2-emulator/temperature-ds18b20', data={'house-code': 'FA-32', 'temperature-ds18b20': '10.123'})
        hc = HouseCode.objects.first()
        self.assertEqual(hc.temperature_ds18b20, 10.123)

    def test_alphabetical_input(self):
        hc = HouseCode.objects.create(code='FA-32')
        data = {'house-code': hc.code, 'temperature-ds18b20': 'asdf'}
        response = self.client.post('/rev2-emulator/temperature-ds18b20', data=data)
        response = json.loads(response.content)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(response['errors'], [api.models.INVALID_TEMPERATURE_DS18B20_MSG.format('asdf')])

    def test_invalid_precision(self):
        hc = HouseCode.objects.create(code='FA-32')
        data = {'house-code': hc.code, 'temperature-ds18b20': '12.22223'}
        response = self.client.post('/rev2-emulator/temperature-ds18b20', data=data)
        response = json.loads(response.content)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(response['errors'], [api.models.INVALID_TEMPERATURE_DS18B20_MSG.format('12.22223')])
        
class SwitchViewTest(TestCase):

    def test_url(self):
        found = resolve('/rev2-emulator/switch')
        self.assertEqual(found.func, rev2_emulator.views.switch_view)
    
    def test_post_updates(self):
        hc = HouseCode.objects.create(code="FA-32")
        response = self.client.post('/rev2-emulator/switch', data={'house-code': 'FA-32', 'switch': 'on'})
        hc = HouseCode.objects.first()
        self.assertEqual(hc.switch, 'on')

class SynchronisingViewTest(TestCase):

    def test_url(self):
        found = resolve('/rev2-emulator/synchronising')
        self.assertEqual(found.func, rev2_emulator.views.synchronising_view)
    
    def test_post_updates(self):
        hc = HouseCode.objects.create(code="FA-32")
        response = self.client.post('/rev2-emulator/synchronising', data={'house-code': 'FA-32', 'synchronising': 'on'})
        hc = HouseCode.objects.first()
        self.assertEqual(hc.synchronising, 'on')

class RelativeHumidityViewTest(TestCase):

    def test_url(self):
        found = resolve('/rev2-emulator/relative-humidity')
        self.assertEqual(found.func, rev2_emulator.views.relative_humidity_view)
    
    def test_post_updates(self):
        hc = HouseCode.objects.create(code="FA-32")
        response = self.client.post('/rev2-emulator/relative-humidity', data={'house-code': 'FA-32', 'relative-humidity': '50'})
        hc = HouseCode.objects.first()
        self.assertEqual(hc.relative_humidity, 50)

class WindowViewTest(TestCase):

    def test_url(self):
        found = resolve('/rev2-emulator/window')
        self.assertEqual(found.func, rev2_emulator.views.window_view)
    
    def test_post_updates(self):
        hc = HouseCode.objects.create(code="FA-32")
        response = self.client.post('/rev2-emulator/window', data={'house-code': 'FA-32', 'window': 'open'})
        hc = HouseCode.objects.first()
        self.assertEqual(hc.window, 'open')

class LastUpdatedAllViewTest(TestCase):

    def test_url(self):
        found = resolve('/rev2-emulator/last-updated-all')
        self.assertEqual(found.func, rev2_emulator.views.last_updated_all_view)
    
    def test_post_updates(self):
        hc = HouseCode.objects.create(code="FA-32")
        response = self.client.post('/rev2-emulator/last-updated-all', data={'house-code': 'FA-32', 'last-updated-all': '2015-07-17T16:07:39.646127'})
        hc = HouseCode.objects.first()
        x = datetime.datetime.strptime('2015-07-17T16:07:39.646127Z', "%Y-%m-%dT%H:%M:%S.%fZ")
        x = timezone.make_aware(x, timezone.get_current_timezone())
        self.assertEqual(hc.last_updated_all, x)

class LastUpdatedTemperatureViewTest(TestCase):

    def test_url(self):
        found = resolve('/rev2-emulator/last-updated-temperature')
        self.assertEqual(found.func, rev2_emulator.views.last_updated_temperature_view)
    
    def test_post_updates(self):
        hc = HouseCode.objects.create(code="FA-32")
        response = self.client.post(
            '/rev2-emulator/last-updated-temperature',
            data={'house-code': 'FA-32', 'last-updated-temperature': '2015-07-17T16:07:39.646127'}
        )
        hc = HouseCode.objects.first()
        x = datetime.datetime.strptime('2015-07-17T16:07:39.646127Z', "%Y-%m-%dT%H:%M:%S.%fZ")
        x = timezone.make_aware(x, timezone.get_current_timezone())
        self.assertEqual(hc.last_updated_temperature, x)

