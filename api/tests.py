import json
import api.views
from django.test import TestCase
from api.views import api_documentation
from django.core.urlresolvers import resolve
from ors.models import HouseCode

class ApiDocumentationTest(TestCase):

    def test_api_url_resolves_to_api_documentation(self):
        found = resolve('/api/')
        self.assertEqual(found.func, api_documentation)

    def test_uses_template(self):
        response = self.client.get('/api/')
        self.assertTemplateUsed(response, 'api/api_documentation.html')

    def test_api_list_is_passed(self):
        response = self.client.get('/api/')
        self.assertTrue('list' in response.context)
                              
class ApiHouseCodesTest(TestCase):
    
    def test_house_codes_url(self):
        found = resolve('/api/house-codes')
        self.assertEqual(found.func, api.views.house_codes)

    def test_GET_returns_house_codes(self):
        HouseCode.objects.create(code='HouseCode')
        response = self.client.get('/api/house-codes')
        house_codes = json.loads(response.content)['content']
        self.assertIn('HouseCode', house_codes)
        
    def validate_json_object_format(self, response):
        self.assertIn(response.content_type, ['application/json', 'json'])
        dict_ = json.load(response.content)
        self.assertIn(dict_, 'status')
        self.assertIn(dict_, 'content')
