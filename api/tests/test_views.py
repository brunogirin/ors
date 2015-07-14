from functools import wraps
import json
import api.views
from django.test import TestCase
from api.views import api_documentation, INVALID_INPUT_STATUS
from django.core.urlresolvers import resolve
from ors.models import HouseCode
from api.forms import ValveForm


class ApiViewTest(TestCase):

    def setUp(self):
        # wrap the client's post and get method to validate the response format
        self.client.post = self.response_wrapper(self.client.post)
        self.client.get = self.response_wrapper(self.client.get)

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

class ApiValveTest(ApiViewTest):

    def test_api_url_resolves_valve(self):
        found = resolve('/api/valve/house-code')
        self.assertEqual(found.func, api.views.valve_view)

    def test_main(self): # TODO: Need to know what the response should look like
        response = self.client.post("/api/valve/house-code")

    def test_open_input(self):
        # empty
        response = self.client.post('/api/valve/house-code', data={'open-input': '', "min-temp": '7', 'max-temp': '20'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Invalid input for parameter: open. Received: , expected: 0-100"])

        # below min
        response = self.client.post('/api/valve/house-code', data={'open-input': '-1', "min-temp": '7', 'max-temp': '20'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Invalid input for parameter: open. Received: -1, expected: 0-100"])

        # above max
        response = self.client.post('/api/valve/house-code', data={'open-input': '101', "min-temp": '7', 'max-temp': '20'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Invalid input for parameter: open. Received: 101, expected: 0-100"])

        # non int
        response = self.client.post('/api/valve/house-code', data={'open-input': 'a', "min-temp": '7', 'max-temp': '20'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Invalid input for parameter: open. Received: a, expected: 0-100"])
        
    def test_min_temp_input(self):
        # empty
        response = self.client.post('/api/valve/house-code', data={'open-input': '50', "min-temp": '', 'max-temp': '20'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Invalid input for parameter: min-temp. Received: , expected: 7-28"])

        # below min
        response = self.client.post('/api/valve/house-code', data={'open-input': '50', "min-temp": '6', 'max-temp': '20'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Invalid input for parameter: min-temp. Received: 6, expected: 7-28"])

        # above max
        response = self.client.post('/api/valve/house-code', data={'open-input': '50', "min-temp": '29', 'max-temp': '20'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertIn("Invalid input for parameter: min-temp. Received: 29, expected: 7-28", errors)

        # non int
        response = self.client.post('/api/valve/house-code', data={'open-input': '50', "min-temp": 'a', 'max-temp': '20'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Invalid input for parameter: min-temp. Received: a, expected: 0-100"])

    def test_max_temp_input(self):
        # empty
        response = self.client.post('/api/valve/house-code', data={'open-input': '50', "min-temp": '7', 'max-temp': ''})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Invalid input for parameter: max-temp. Received: , expected: 7-28"])

        # below min
        response = self.client.post('/api/valve/house-code', data={'open-input': '50', "min-temp": '7', 'max-temp': '6'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertIn(["Invalid input for parameter: max-temp. Received: 6, expected: 7-28"], errors)

        # above max
        response = self.client.post('/api/valve/house-code', data={'open-input': '50', "min-temp": '7', 'max-temp': '29'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertIn("Invalid input for parameter: max-temp. Received: 29, expected: 7-28", errors)

        # non int
        response = self.client.post('/api/valve/house-code', data={'open-input': '50', "min-temp": '7', 'max-temp': 'a'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertIn("Invalid input for parameter: max-temp. Received: a, expected: 7-28", errors)

    def test_max_temp_greater_than_min_temp(self):
        response = self.client.post('/api/valve/house-code', data={'open-input': '50', 'min-temp': '20', 'max-temp': '20'})
        errors = json.loads(response.content)['errors']
        self.assertEqual(errors, ["Invalid input for parameter: max-temp. max-temp (20) must be greater than min-temp (20)"])

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
                              
class ApiHouseCodesTest(ApiViewTest):

    def test_POST_blank_does_not_save(self):
        self.client.post("/api/house-codes", data={"house-codes": ""})
        self.assertEqual(HouseCode.objects.count(), 0)

    def test_POST_blank_returns_blank_house_code_warning(self):
        response = json.loads(self.client.post("/api/house-codes", data={"house-codes": ""}).content)
        self.assertIn("warnings", response)
        self.assertEqual(response["warnings"], ["ignored empty house code(s)"])

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

