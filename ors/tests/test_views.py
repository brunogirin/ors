import json
import ors.views
import api.views
from django.test import TestCase
from ors.views import home
from django.core.urlresolvers import resolve
from api.views import INVALID_INPUT_STATUS
from api.models import HOUSE_CODE_NOT_FOUND_MSG

from api.forms import ValveForm

class LedViewTest(TestCase):

    def test_url_resolves(self):
        found = resolve('/led/house-code')
        self.assertEqual(found.func, ors.views.led_view)

    def test_house_code_does_not_exist(self):
        response = self.client.post('/led/house-code', data={'house-code': 'E2-E1'})
        response = json.loads(response.content)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(response['errors'], [HOUSE_CODE_NOT_FOUND_MSG.format('E2-E1')])

class HomePageTest(TestCase):

    def test_home_url_resolves_to_home_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_uses_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'ors/home.html')

class EmulatorValveViewTest(TestCase):

    def test_displays_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['valve_form'], ValveForm)


class ValveViewRedirectTest(TestCase):

    def test_api_url_resolves_valve(self):
        found = resolve('/valve/house-code')
        self.assertEqual(found.func, api.views.valve_view_redirect)


