from functools import wraps
import json
import api.views
from django.test import TestCase
from api.views import api_documentation, INVALID_INPUT_STATUS, VALID_COLOURS, VALID_FLASH
from django.core.urlresolvers import resolve
from api.models import HouseCode, INVALID_HOUSE_CODE_MSG, HOUSE_CODE_NOT_FOUND_MSG
from api.forms import ValveForm
from api.models import Debug, Led

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
    
    def test_api_url_resolves(self):
        found = resolve('/api/status/house-code')
        self.assertEqual(found.func, api.views.status_view)

    # TODO: Need to know what the model should be
    def test_main(self):
        response = self.client.get('/api/status/house-code')
        response = json.loads(response.content)
        self.assertEqual(response, {'status': 200, 'content': {'relative-humidity': 0, 'temperature-opentrv': 0, 'temperature-ds18b20': 0, 'window': 0, 'switch': 0, 'last-updated-all': 0, 'last-updated-temperature': 0, 'led': 0, 'synchronising': 0, 'ambient-light': 0, 'house-code': 0}})

class ApiLedTest(ApiViewTest):
    
    def test_api_url_resolves(self):
        found = resolve('/api/led/house-code')
        self.assertEqual(found.func, api.views.led_view)

    # TODO: Need to know that the response looks like to test it
    def test_valid_arguments(self):
        response = self.client.post('/api/led/house-code', data={'colour': '0', 'flash': '1'})
        response = json.loads(response.content)
        self.assertEqual(response['status'], 200)
        with self.assertRaises(KeyError):
            response['errors']

    def test_missing_arguments(self):
        response = self.client.post('/api/led/house-code')
        response = json.loads(response.content)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(response['errors'], ['Required input parameter: colour', 'Required input parameter: flash'])

    def test_invalid_colour_argument(self):
        # non numeric
        response = self.client.post('/api/led/house-code', data={'colour': 'a', 'flash': '1'})
        response = json.loads(response.content)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(response['errors'], ['Invalid input for parameter: colour. Received: a, expected: {}'.format(VALID_COLOURS)])
        # below min
        response = self.client.post('/api/led/house-code', data={'colour': '-1', 'flash': '1'})
        response = json.loads(response.content)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(response['errors'], ['Invalid input for parameter: colour. Received: -1, expected: {}'.format(VALID_COLOURS)])
        # above max
        response = self.client.post('/api/led/house-code', data={'colour': '4', 'flash': '1'})
        response = json.loads(response.content)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(response['errors'], ['Invalid input for parameter: colour. Received: 4, expected: {}'.format(VALID_COLOURS)])

    def test_invalid_flash_argument(self):
        # non numeric
        response = self.client.post('/api/led/house-code', data={'colour': '0', 'flash': 'a'})
        response = json.loads(response.content)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(response['errors'], ['Invalid input for parameter: flash. Received: a, expected: {}'.format(VALID_FLASH)])
        # not matched
        response = self.client.post('/api/led/house-code', data={'colour': '0', 'flash': '20'})
        response = json.loads(response.content)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(response['errors'], ['Invalid input for parameter: flash. Received: 20, expected: {}'.format(VALID_FLASH)])

    def test_setting_attributes(self):
        Led.objects.create(colour=0, flash=1)
        response = self.client.post('/api/led/house-code', data={'colour': '1', 'flash': '2'})
        response = json.loads(response.content)
        self.assertEqual(response['status'], 200)
        self.assertEqual(Led.objects.first().colour, 1) # colour
        self.assertEqual(Led.objects.first().flash, 2) # flash

    def test_changing_state_does_not_add_more_debug_objects(self):
        Led.objects.create(colour=0, flash=1)
        self.client.post('/api/led/house-code', data={'colour': '1', 'flash': '2'})
        self.client.post('/api/led/house-code', data={'colour': '3', 'flash': '4'})
        self.assertEqual(Led.objects.count(), 1)

class ApiDebugTest(ApiViewTest):

    def test_api_url_resolves(self):
        found = resolve('/api/debug')
        self.assertEqual(found.func, api.views.debug_view)
    
    def test_missing_arguments_returns_error(self):
        response = self.client.post('/api/debug')
        response = json.loads(response.content)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(response['errors'], ['Required input parameter: state'])

    def test_invalid_arguments_returns_error(self):
        response = self.client.post('/api/debug', data={'state': 'ON'})
        response = json.loads(response.content)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(response['errors'], ['Invalid input for parameter: state. Received: ON, expected: on/off'])

    def test_post_state_on_turns_debug_on(self):
        self.client.post('/api/debug', data={'state': 'on'})
        self.assertEqual(Debug.objects.first().state, 'on')

    def test_post_state_off_turns_debug_off(self):
        self.client.post('/api/debug', data={'state': 'off'})
        self.assertEqual(Debug.objects.first().state, 'off')

    def test_changing_state_does_not_add_more_debug_objects(self):
        self.client.post('/api/debug', data={'state': 'on'})
        self.client.post('/api/debug', data={'state': 'off'})
        self.assertEqual(Debug.objects.count(), 1)

    def test_changing_state(self):
        self.client.post('/api/debug', data={'state': 'on'})
        self.assertEqual(Debug.objects.first().state, 'on')
        self.client.post('/api/debug', data={'state': 'off'})
        self.assertEqual(Debug.objects.first().state, 'off')

    def test_get_returns_default(self):
        response = self.client.get('/api/debug')
        response = json.loads(response.content)
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['content'], 'off')

    def test_get_on(self):
        Debug.objects.create(state="on")
        response = self.client.get('/api/debug')
        response = json.loads(response.content)
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['content'], 'on')

    def test_get_off(self):
        Debug.objects.create(state="off")
        response = self.client.get('/api/debug')
        response = json.loads(response.content)
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['content'], 'off')

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
        
    def test_min_temp_input(self):
        # not provided
        HouseCode.objects.create(code="FA-32")
        response = self.client.post('/api/valve/FA-32', data={'open_input': '50', 'max_temp': '20'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Required input parameter: min_temp"])
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)

        # empty
        response = self.client.post('/api/valve/FA-32', data={'open_input': '50', "min_temp": '', 'max_temp': '20'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Invalid input for parameter: min_temp. Received: , expected: 7-28"])
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)

        # below min
        response = self.client.post('/api/valve/FA-32', data={'open_input': '50', "min_temp": '6', 'max_temp': '20'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Invalid input for parameter: min_temp. Received: 6, expected: 7-28"])
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)

        # above max
        response = self.client.post('/api/valve/FA-32', data={'open_input': '50', "min_temp": '29', 'max_temp': '20'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertIn("Invalid input for parameter: min_temp. Received: 29, expected: 7-28", errors)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)

        # non int
        response = self.client.post('/api/valve/FA-32', data={'open_input': '50', "min_temp": 'a', 'max_temp': '20'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Invalid input for parameter: min_temp. Received: a, expected: 7-28"])
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)

    def test_max_temp_input(self):
        # not provided
        HouseCode.objects.create(code="FA-32")
        response = self.client.post('/api/valve/FA-32', data={"open_input": '50', "min_temp": '7'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Required input parameter: max_temp"])
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)

        # empty
        response = self.client.post('/api/valve/FA-32', data={'open_input': '50', "min_temp": '7', 'max_temp': ''})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Invalid input for parameter: max_temp. Received: , expected: 7-28"])
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)

        # below min
        response = self.client.post('/api/valve/FA-32', data={'open_input': '50', "min_temp": '7', 'max_temp': '6'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertIn("Invalid input for parameter: max_temp. Received: 6, expected: 7-28", errors)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)

        # above max
        response = self.client.post('/api/valve/FA-32', data={'open_input': '50', "min_temp": '7', 'max_temp': '29'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertIn("Invalid input for parameter: max_temp. Received: 29, expected: 7-28", errors)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)

        # non int
        response = self.client.post('/api/valve/FA-32', data={'open_input': '50', "min_temp": '7', 'max_temp': 'a'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertIn("Invalid input for parameter: max_temp. Received: a, expected: 7-28", errors)
        self.assertEqual(response['status'], INVALID_INPUT_STATUS)

    def test_max_temp_greater_than_min_temp(self):
        HouseCode.objects.create(code="FA-32")
        response = self.client.post('/api/valve/FA-32', data={'open_input': '50', 'min_temp': '20', 'max_temp': '20'})
        response = json.loads(response.content)
        errors = response['errors']
        self.assertEqual(errors, ["Invalid input for parameter: max_temp. max_temp (20) must be greater than min_temp (20)"])
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
        self.assertEqual(response['errors'], ["Invalid house-code. Recieved: WX-YZ, expected XX-XX where XX are uppercase hex numbers"])
        self.assertEqual(response['content'], [])

    def test_POST_blank_does_not_save(self):
        self.client.post("/api/house-codes", data={"house-codes": ""})
        self.assertEqual(HouseCode.objects.count(), 0)

    def test_POST_blank_returns_error(self):
        response = json.loads(self.client.post("/api/house-codes", data={"house-codes": ""}).content)
        self.assertIn("errors", response)
        self.assertIn("Invalid house-code. Recieved: , expected XX-XX where XX are uppercase hex numbers", response["errors"])

    def test_POST_saves_a_house_code(self):
        response = self.client.post("/api/house-codes", data={"house-codes": "FA-32"})
        self.assertEqual(HouseCode.objects.count(), 1)
        house_code = HouseCode.objects.first()
        self.assertEqual(house_code.code, "FA-32")

    def test_POST_can_save_multiple_house_codes(self):
        response = self.client.post("/api/house-codes", data={"house-codes": " FA-32, E2-E1,45-40"}) 
        self.assertEqual(HouseCode.objects.count(), 3)
        iter = HouseCode.objects.iterator()
        housecode1 = iter.next()
        housecode2 = iter.next()
        housecode3 = iter.next()
        self.assertEqual(housecode1.code, "FA-32")
        self.assertEqual(housecode2.code, "E2-E1")
        self.assertEqual(housecode3.code, "45-40")

    def test_POST_overwrites_existing_house_codes(self):
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

    def test_POST_replacing_same_housecode_does_not_raise_error(self):
        response = self.client.post('/api/house-codes', data={'house-codes': 'FA-32'})
        response = self.client.post('/api/house-codes', data={'house-codes': 'FA-32, E2-E1'})
        response = json.loads(response.content)
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['content'], ['FA-32', 'E2-E1'])

        
