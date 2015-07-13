from django.test import TestCase
from ors.views import home
from django.core.urlresolvers import resolve

class HomePageTest(TestCase):

    def test_home_url_resolves_to_home_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_uses_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'ors/home.html')
