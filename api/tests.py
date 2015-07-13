from functools import wraps
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

    def setUp(self):
        # wrap the client's post and get method to validate the response format
        self.client.post = self.response_wrapper(self.client.post)
        self.client.get = self.response_wrapper(self.client.get)

    def test_POST_saves_a_house_code(self):
        response = self.client.post("/api/house-codes", data={"house-codes": "housecode1"})
        self.assertEqual(HouseCode.objects.count(), 1)
        house_code = HouseCode.objects.first()
        self.assertEqual(house_code.code, "housecode1")

    def test_POST_can_save_multiple_house_codes(self):
        response = self.client.post("/api/house-codes", data={"house-codes": "housecode1\r\nhousecode2\r\nhousecode3"}) 
        self.assertEqual(HouseCode.objects.count(), 3)
        iter = HouseCode.objects.iterator()
        housecode1 = iter.next()
        housecode2 = iter.next()
        housecode3 = iter.next()
        self.assertEqual(housecode1.code, "housecode1")
        self.assertEqual(housecode2.code, "housecode2")
        self.assertEqual(housecode3.code, "housecode3")

    def test_POST_overwrites_existing_house_codes(self):
        response = self.client.post("/api/house-codes", data={"house-codes": "housecode1\r\nhousecode2\r\nhousecode3"}) 
        response = self.client.post("/api/house-codes", data={"house-codes": "new_housecode1\r\nnew_housecode2\r\nnew_housecode3"}) 
        self.assertEqual(HouseCode.objects.count(), 3)
        iter = HouseCode.objects.iterator()
        housecode1 = iter.next()
        housecode2 = iter.next()
        housecode3 = iter.next()
        self.assertEqual(housecode1.code, "new_housecode1")
        self.assertEqual(housecode2.code, "new_housecode2")
        self.assertEqual(housecode3.code, "new_housecode3")
    
    def test_house_codes_url(self):
        found = resolve('/api/house-codes')
        self.assertEqual(found.func, api.views.house_codes)

    def test_GET_returns_house_codes(self):
        HouseCode.objects.create(code='HouseCode')
        response = self.client.get('/api/house-codes')
        house_codes = json.loads(response.content)['content']
        self.assertIn('HouseCode', house_codes)

    def validate_json_object_format(self, response):
        self.assertEqual(response['Content-Type'], 'application/json')
        dict_ = json.loads(response.content)
        self.assertIn('status', dict_)
        self.assertEqual(type(dict_['status']), int)
        self.assertIn('content', dict_)

    def response_wrapper(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            self.validate_json_object_format(response)
            return response
        return wrapper
