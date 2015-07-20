import datetime
import rev2_emulator.views
from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpResponse, JsonResponse
from api.models import HouseCode

# Create your tests here.

class EmulatorViewTest(TestCase):

    def test_url(self):
        found = resolve('/rev2-emulator/')
        self.assertEqual(found.func, rev2_emulator.views.emulator_view)
        
    def test_template(self):
        response = self.client.get('/rev2-emulator/')
        self.assertTemplateUsed(response, 'rev2_emulator/home.html')

    def test_post_redirects_to_api_web_page(self):
        hc = HouseCode.objects.create(code="FA-32")
        response = self.client.post('/rev2-emulator/', data={'room-temp': '23.125', 'house-code': 'FA-32'})
        self.assertRedirects(response, '/')

    def test_post_updates_temperature(self):
        hc = HouseCode.objects.create(code="FA-32")
        response = self.client.post('/rev2-emulator/', data={'room-temp': '23.125', 'house-code': 'FA-32'})
        hc = HouseCode.objects.get(code="FA-32")
        self.assertEqual(hc.temperature_opentrv, '23.125')

    def test_invalid_input_redirects_to_the_same_page(self):
        response = self.client.post('/rev2-emulator/')
        self.assertRedirects(response, '/rev2-emulator/')

class TemperatureOpentrvViewTest(TestCase):

    def test_url(self):
        found = resolve('/rev2-emulator/temperature-opentrv')
        self.assertEqual(found.func, rev2_emulator.views.temperature_opentrv_view)
    
    def test_post_updates(self):
        hc = HouseCode.objects.create(code="FA-32")
        response = self.client.post('/rev2-emulator/temperature-opentrv', data={'house-code': 'FA-32', 'room-temp': '10.123'})
        hc = HouseCode.objects.first()
        self.assertEqual(hc.temperature_opentrv, '10.123')

class TemperatureDs18b20ViewTest(TestCase):

    def test_url(self):
        found = resolve('/rev2-emulator/temperature-ds18b20')
        self.assertEqual(found.func, rev2_emulator.views.temperature_ds18b20_view)
    
    def test_post_updates(self):
        hc = HouseCode.objects.create(code="FA-32")
        response = self.client.post('/rev2-emulator/temperature-ds18b20', data={'house-code': 'FA-32', 'temperature-ds18b20': '10.123'})
        hc = HouseCode.objects.first()
        self.assertEqual(hc.temperature_ds18b20, '10.123')

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

