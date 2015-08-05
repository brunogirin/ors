import rev2
import mock
from mock import Mock, patch
from functools import wraps
import json
import api.views
from django.test import TestCase
from api.views import api_documentation, INVALID_INPUT_STATUS
from api.views import INVALID_LED_COLOUR_MSG, INVALID_LED_STATE_MSG, INVALID_LED_REPEAT_INTERVAL_MSG
from api.views import MISSING_LED_COLOUR_MSG, MISSING_LED_STATE_MSG, MISSING_LED_REPEAT_INTERVAL_MSG
from django.core.urlresolvers import resolve
from api.models import HouseCode, INVALID_HOUSE_CODE_MSG, HOUSE_CODE_NOT_FOUND_MSG
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

class ApiStatusTest(ApiViewTest):

    maxDiff = None
    
    def test_api_url_resolves(self):
        found = resolve('/api/status/house-code')
        self.assertEqual(found.func, api.views.status_view)

    # TODO - Add other attributes of the house code
    @patch('api.models.HouseCode.to_dict')
    def test_returns_house_code_values(self, to_dict_mock):
        house_code = HouseCode.objects.create(code='FA-32', temperature_opentrv='23.125')
        expected_content = {'house-code': 'FA-32'}
        to_dict_mock.return_value = expected_content
        response = self.client.get('/api/status/FA-32')
        response = json.loads(response.content)
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['content'], expected_content)
        to_dict_mock.called_once_with()
        
class ApiLedTest(ApiViewTest):
    
    def test_api_url_resolves(self):
        found = resolve('/api/led/house-code')
        self.assertEqual(found.func, api.views.led_view)

    def test_non_existent_house_code(self):
        response = self.client.post('/api/led/FA-32', data={})
        response = json.loads(response.content)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        self.assertIn(HOUSE_CODE_NOT_FOUND_MSG.format('FA-32'), response['errors'])

    def test_blank_colour(self):
        hc = HouseCode.objects.create(code='FA-32')
        response = self.client.post('/api/led/FA-32', data={'colour': ''})
        response = json.loads(response.content)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        self.assertIn(INVALID_LED_COLOUR_MSG.format(''), response['errors'])

    def test_no_parameters(self):
        hc = HouseCode.objects.create(code='FA-32')
        response = self.client.post('/api/led/FA-32')
        response = json.loads(response.content)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        self.assertIn(MISSING_LED_COLOUR_MSG, response['errors'])
        self.assertIn(MISSING_LED_STATE_MSG, response['errors'])
        self.assertIn(MISSING_LED_REPEAT_INTERVAL_MSG, response['errors'])

    def test_blank_state(self):
        hc = HouseCode.objects.create(code='FA-32')
        response = self.client.post('/api/led/FA-32', data={'state': ''})
        response = json.loads(response.content)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        self.assertIn(INVALID_LED_STATE_MSG.format(''), response['errors'])

    def test_blank_repeat_interval(self):
        hc = HouseCode.objects.create(code='FA-32')
        response = self.client.post('/api/led/FA-32', data={'repeat-interval': ''})
        response = json.loads(response.content)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        self.assertIn(INVALID_LED_REPEAT_INTERVAL_MSG.format(''), response['errors'])

class ApiDebugTest(ApiViewTest):

    def test_api_url_resolves(self):
        found = resolve('/api/debug/FA-32')
        self.assertEqual(found.func, api.views.debug_view)

    def test_non_existent_house_code(self):
        response = self.client.post('/api/debug/FA-32')
        response = json.loads(response.content)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        self.assertIn(HOUSE_CODE_NOT_FOUND_MSG.format('FA-32'), response['errors'])
        
class ApiValveTest(ApiViewTest):

    def test_api_url_resolves_valve(self):
        found = resolve('/api/valve/FA-32')
        self.assertEqual(found.func, api.views.valve_view)

    def test_house_code_input(self):
        response = self.client.post('/api/valve/')
        response = json.loads(response.content)
        errors = response['errors']
        self.assertIn(HOUSE_CODE_NOT_FOUND_MSG.format(''), errors)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        response = self.client.post('/api/valve/HOUSECODE')
        response = json.loads(response.content)
        errors = response['errors']
        self.assertIn(HOUSE_CODE_NOT_FOUND_MSG.format('HOUSECODE'), errors)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)

    def test_non_existant_house_code_returns_error(self):
        response = self.client.post('/api/valve/FA-32', data={'open_input': '50', "min_temp": '7', 'max_temp': '20'})
        response = json.loads(response.content)
        self.assertEqual(response['errors'], [HOUSE_CODE_NOT_FOUND_MSG.format('FA-32')])
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)

    def test_open_input(self):
        # not provided
        HouseCode.objects.create(code="FA-32")
        response = self.client.post('/api/valve/FA-32', data={"min_temp": '7', 'max_temp': '20'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Required input parameter: open_input"])
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)

        # empty
        response = self.client.post('/api/valve/FA-32', data={'open_input': '', "min_temp": '7', 'max_temp': '20'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Invalid input for parameter: open_input. Received: , expected: 0-100"])
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)

        # below min
        response = self.client.post('/api/valve/FA-32', data={'open_input': '-1', "min_temp": '7', 'max_temp': '20'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Invalid input for parameter: open_input. Received: -1, expected: 0-100"])
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)

        # above max
        response = self.client.post('/api/valve/FA-32', data={'open_input': '101', "min_temp": '7', 'max_temp': '20'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Invalid input for parameter: open_input. Received: 101, expected: 0-100"])
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)

        # non int
        response = self.client.post('/api/valve/FA-32', data={'open_input': 'a', "min_temp": '7', 'max_temp': '20'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Invalid input for parameter: open_input. Received: a, expected: 0-100"])
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)

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

    def test_invalid_format(self):
        response = self.client.post("/api/house-codes", data={"house-codes": "WX-YZ"})
        response = json.loads(response.content)
        self.assertEqual(response['errors'], ['Invalid input for "house-code". Recieved: WX-YZ, expected XX-XX where XX are uppercase hex numbers'])
        self.assertEqual(response['content'], [])
        
    @patch('rev2.poll')
    def test_POST_initialises_cache(self, mock_poll):
        def side_effect(house_code):
            house_code.relative_humidity = 50
        mock_poll.side_effect = side_effect
        response = self.client.post('/api/house-codes', data={'house-codes': 'FA-32'})
        response = self.client.get('/api/status/FA-32')
        response = json.loads(response.content)
        response = response['content']
        self.assertEqual(response['relative-humidity'], 50)

    def test_POST_blank_does_not_save(self):
        self.client.post("/api/house-codes", data={"house-codes": ""})
        self.assertEqual(HouseCode.objects.count(), 0)

    def test_POST_blank_returns_error(self):
        response = json.loads(self.client.post("/api/house-codes", data={"house-codes": ""}).content)
        self.assertIn("errors", response)
        self.assertIn('Invalid input for "house-code". Recieved: , expected XX-XX where XX are uppercase hex numbers', response["errors"])

    @patch('rev2.poll')
    def test_POST_saves_a_house_code(self, mock_poll):
        response = self.client.post("/api/house-codes", data={"house-codes": "FA-32"})
        self.assertEqual(HouseCode.objects.count(), 1)
        house_code = HouseCode.objects.first()
        self.assertEqual(house_code.code, "FA-32")

    @patch('rev2.poll')
    def test_POST_can_save_multiple_house_codes(self, mock_poll):
        response = self.client.post("/api/house-codes", data={"house-codes": " FA-32, E2-E1,45-40"}) 
        self.assertEqual(HouseCode.objects.count(), 3)
        iter = HouseCode.objects.iterator()
        housecode1 = iter.next()
        housecode2 = iter.next()
        housecode3 = iter.next()
        self.assertEqual(housecode1.code, "FA-32")
        self.assertEqual(housecode2.code, "E2-E1")
        self.assertEqual(housecode3.code, "45-40")

    @patch('rev2.poll')
    def test_POST_overwrites_existing_house_codes(self, mock_poll):
        response = self.client.post("/api/house-codes", data={"house-codes": "FA-32, E2-E1, 45-40"}) 
        response = self.client.post("/api/house-codes", data={"house-codes": "FA-33, E2-E2, 45-41"}) 
        self.assertEqual(HouseCode.objects.count(), 3)
        iter = HouseCode.objects.iterator()
        housecode1 = iter.next()
        housecode2 = iter.next()
        housecode3 = iter.next()
        self.assertIsNotNone(HouseCode.objects.get(code="FA-33"))
        self.assertIsNotNone(HouseCode.objects.get(code="E2-E2"))
        self.assertIsNotNone(HouseCode.objects.get(code="45-41"))
    
    def test_house_codes_url(self):
        found = resolve('/api/house-codes')
        self.assertEqual(found.func, api.views.house_codes)

    def test_GET_returns_house_codes(self):
        HouseCode.objects.create(code='HouseCode')
        response = self.client.get('/api/house-codes')
        house_codes = json.loads(response.content)['content']
        self.assertIn('HouseCode', house_codes)

    @patch('rev2.poll')
    def test_POST_replacing_same_housecode_does_not_raise_error(self, mock_poll):
        response = self.client.post('/api/house-codes', data={'house-codes': 'FA-32'})
        response = self.client.post('/api/house-codes', data={'house-codes': 'FA-32, E2-E1'})
        response = json.loads(response.content)
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['content'], ['FA-32', 'E2-E1'])

        
