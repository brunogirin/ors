import rev2_emulator.views
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
