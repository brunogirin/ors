import api.views
from django.test import TestCase
from ors.views import home
from django.core.urlresolvers import resolve

from api.forms import ValveForm

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
        found = resolve('/api/valve/house-code')
        self.assertEqual(found.func, api.views.valve_view_redirect)

