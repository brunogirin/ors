import mock
import json
import api.models
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.common.by import By
from .base import FunctionalTest
from api.views import INVALID_INPUT_STATUS, VALID_LED_COLOURS, VALID_LED_STATES, VALID_LED_REPEAT_INTERVALS, INVALID_HOUSE_CODE_MSG
from api.models import HOUSE_CODE_NOT_FOUND_MSG, HouseCode
from mock import patch

class Rev2EmulatorTest(FunctionalTest):

    def test_house_code_not_found(self):
        # do this to get the csrf token
        self.browser.get(self.server_url)
        
        # user goes to the rev2 emulator page
        self.initialise_page()

        # user does not input a house code
        # user inputs a new temperature-opentrv
        self.temperature_opentrv_input.send_keys('23.333\n')
        self.response_section = self.browser.find_element_by_id('id-response-section')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(json_response['errors'], [api.models.HOUSE_CODE_NOT_FOUND_MSG.format('')])

        # user inputs a new temperature-opentrv
        # user inputs a house code that is not in the database
        self.house_code_input.send_keys('FA-32')
        self.temperature_opentrv_input.clear()
        self.temperature_opentrv_input.send_keys('23.333\n')
        self.response_section = self.browser.find_element_by_id('id-response-section')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(json_response['errors'], [api.models.HOUSE_CODE_NOT_FOUND_MSG.format('FA-32')])
        
        # user inputs a new temperature-ds18b20
        # user inputs a house code that is not in the database
        self.temperature_ds18b20_input.send_keys('23.333\n')
        self.response_section = self.browser.find_element_by_id('id-response-section')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(json_response['errors'], [api.models.HOUSE_CODE_NOT_FOUND_MSG.format('FA-32')])

        # user inputs a new window
        # user inputs a house code that is not in the database
        self.window_input.send_keys('open\n')
        self.response_section = self.browser.find_element_by_id('id-response-section')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(json_response['errors'], [api.models.HOUSE_CODE_NOT_FOUND_MSG.format('FA-32')])

        # user inputs a new switch
        # user inputs a house code that is not in the database
        self.switch_input.send_keys('on\n')
        self.response_section = self.browser.find_element_by_id('id-response-section')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(json_response['errors'], [api.models.HOUSE_CODE_NOT_FOUND_MSG.format('FA-32')])

        # user inputs a new last-updated-all
        # user inputs a house code that is not in the database
        self.last_updated_all_input.send_keys('2015-07-22\n')
        self.response_section = self.browser.find_element_by_id('id-response-section')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(json_response['errors'], [api.models.HOUSE_CODE_NOT_FOUND_MSG.format('FA-32')])

        # user inputs a new last-updated-temperature
        # user inputs a house code that is not in the database
        self.last_updated_temperature_input.send_keys('2015-07-22\n')
        self.response_section = self.browser.find_element_by_id('id-response-section')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(json_response['errors'], [api.models.HOUSE_CODE_NOT_FOUND_MSG.format('FA-32')])

        # user inputs a new synchronising
        # user inputs a house code that is not in the database
        self.synchronising_input.send_keys('on\n')
        self.response_section = self.browser.find_element_by_id('id-response-section')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(json_response['errors'], [api.models.HOUSE_CODE_NOT_FOUND_MSG.format('FA-32')])

        # user inputs a new ambient-light
        # user inputs a house code that is not in the database
        self.ambient_light_input.send_keys('155\n')
        self.response_section = self.browser.find_element_by_id('id-response-section')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(json_response['errors'], [api.models.HOUSE_CODE_NOT_FOUND_MSG.format('FA-32')])

    def test_invalid_inputs(self):

        # user goes to the api page and enters a house code
        self.post_house_code('FA-32')

        # user goes to the rev2 emulator page
        self.initialise_page()

        # user inputs the house code entered earlier
        self.house_code_input.send_keys('FA-32')

        # user inputs an invalid temperature-opentrv
        self.temperature_opentrv_input.send_keys('asdf\n')
        # user notices the response section
        self.response_section = self.browser.find_element_by_id('id-response-section')
        self.response_header = self.response_section.find_element_by_tag_name("h2")
        self.assertEqual(self.response_header.text, "Response")
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(json_response['errors'], [api.models.INVALID_TEMPERATURE_OPENTRV_MSG.format('asdf')])
        # user inputs an invalid temperature-opentrv with too many characters
        self.temperature_opentrv_input.clear()
        self.temperature_opentrv_input.send_keys('23.3333\n')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertIn(api.models.INVALID_TEMPERATURE_OPENTRV_MSG.format('23.3333'), json_response['errors'])
        # user inputs an temperature greater than max
        self.temperature_opentrv_input.clear()
        self.temperature_opentrv_input.send_keys('100.0\n')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertIn(api.models.INVALID_TEMPERATURE_OPENTRV_MSG.format('100.0'), json_response['errors'])
        # user inputs an temperature less than min
        self.temperature_opentrv_input.clear()
        self.temperature_opentrv_input.send_keys('-10.0\n')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertIn(api.models.INVALID_TEMPERATURE_OPENTRV_MSG.format('-10.0'), json_response['errors'])
        # user inputs blank
        self.temperature_opentrv_input.clear()
        self.temperature_opentrv_input.send_keys('\n')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertIn(api.models.INVALID_TEMPERATURE_OPENTRV_MSG.format(''), json_response['errors'])

        
        # user inputs an invalid temperature-ds18b20
        self.temperature_ds18b20_input.send_keys('asdf\n')
        # user notices the response section
        self.response_section = self.browser.find_element_by_id('id-response-section')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(json_response['errors'], [api.models.INVALID_TEMPERATURE_DS18B20_MSG.format('asdf')])
        # user inputs an invalid temperature-ds18b20 with too many characters
        self.temperature_ds18b20_input.clear()
        self.temperature_ds18b20_input.send_keys('23.3333\n')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertIn(api.models.INVALID_TEMPERATURE_DS18B20_MSG.format('23.3333'), json_response['errors'])
        # user inputs an temperature greater than max
        self.temperature_ds18b20_input.clear()
        self.temperature_ds18b20_input.send_keys('100.0\n')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertIn(api.models.INVALID_TEMPERATURE_DS18B20_MSG.format('100.0'), json_response['errors'])
        # user inputs an temperature less than min
        self.temperature_ds18b20_input.clear()
        self.temperature_ds18b20_input.send_keys('-10.0\n')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertIn(api.models.INVALID_TEMPERATURE_DS18B20_MSG.format('-10.0'), json_response['errors'])

        # user inputs an invalid window state
        self.window_input.send_keys('ajar\n')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertIn(api.models.INVALID_WINDOW_STATE_MSG.format('ajar'), json_response['errors'])

        # user inputs an invalid switch state
        self.switch_input.send_keys('halfway\n')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertIn(api.models.INVALID_SWITCH_STATE_MSG.format('halfway'), json_response['errors'])

        # user inputs an invalid last-updated-all date
        self.last_updated_all_input.send_keys('invalid date\n')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, 'id-response-code')))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertIn(api.models.INVALID_LAST_UPDATED_ALL_MSG.format('invalid date'), json_response['errors'])

        # user inputs an invalid last-updated-temperature date
        self.last_updated_temperature_input.send_keys('invalid date\n')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, 'id-response-code')))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertIn(api.models.INVALID_LAST_UPDATED_TEMPERATURE_DATE_MSG.format('invalid date'), json_response['errors'])

        # user inputs an invalid synchronising state
        self.synchronising_input.send_keys('kind of on\n')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertIn(api.models.INVALID_SYNCHRONISING_STATE_MSG.format('kind of on'), json_response['errors'])

        # user inputs an invalid ambient_light state
        self.ambient_light_input.send_keys('33333333\n')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertIn(api.models.INVALID_AMBIENT_LIGHT_VALUE_MSG.format('33333333'), json_response['errors'])

        # user inputs an invalid relative_humidity
        self.relative_humidity_input.send_keys('111\n')
        response_code_element = WebDriverWait(self.browser, timeout=30).until(visibility_of_element_located((By.ID, "id-response-code")))
        json_response = json.loads(response_code_element.text)
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertIn(api.models.INVALID_RELATIVE_HUMIDITY_MSG.format('111'), json_response['errors'])
        
    def initialise_page(self):
        self.browser.get(self.server_url + '/rev2-emulator')
        self.house_code_input = self.browser.find_element_by_id('id-house-code-input')
        self.relative_humidity_form = self.browser.find_element_by_id('id-relative-humidity-form')
        self.relative_humidity_input = self.browser.find_element_by_id('id-relative-humidity-input')
        self.temperature_opentrv_form = self.browser.find_element_by_id('id-temperature-opentrv-form')
        self.temperature_opentrv_input = self.browser.find_element_by_id('id-temperature-opentrv-input')
        self.temperature_ds18b20_form = self.browser.find_element_by_id('id-temperature-ds18b20-form')
        self.temperature_ds18b20_input = self.browser.find_element_by_id('id-temperature-ds18b20-input')
        self.window_form = self.browser.find_element_by_id('id-window-form')
        self.window_input = self.browser.find_element_by_id('id-window-input')
        self.switch_form = self.browser.find_element_by_id('id-switch-form')
        self.switch_input = self.browser.find_element_by_id('id-switch-input')
        self.last_updated_all_form = self.browser.find_element_by_id('id-last-updated-all-form')
        self.last_updated_all_input = self.browser.find_element_by_id('id-last-updated-all-input')
        self.last_updated_temperature_form = self.browser.find_element_by_id('id-last-updated-temperature-form')
        self.last_updated_temperature_input = self.browser.find_element_by_id('id-last-updated-temperature-input')
        self.synchronising_form = self.browser.find_element_by_id('id-synchronising-form')
        self.synchronising_input = self.browser.find_element_by_id('id-synchronising-input')
        self.ambient_light_form = self.browser.find_element_by_id('id-ambient-light-form')
        self.ambient_light_input = self.browser.find_element_by_id('id-ambient-light-input')
        self.get_cached_contents_interval_form = self.browser.find_element_by_id('id-get-cached-contents-interval-form')
        self.get_cached_contents_interval_input = self.browser.find_element_by_id('id-get-cached-contents-interval-input')

    def test_main(self):

        # user goes to the api page and enters a house code
        self.post_house_code('FA-32')

        # user then goes the rev2 emulator page to check it's there
        self.initialise_page()
        self.assertEqual(self.browser.title, "REV2 Emulator")
        self.assertEqual(self.browser.find_element_by_tag_name("h1").text, "REV2 Emulator")
        # user sees the cache after the inputs
        self.assertTrue(self.browser.find_element_by_tag_name("code"))
        # user sees that a default of 4 seconds has been set for the cache refresh rate
        self.assertEqual(self.get_cached_contents_interval_input.get_attribute('value'), '4')
        self.wait_for_attribute_in_cache('FA-32', 'house-code', 'FA-32')
        # user then updates the temperature-opentrv
        self.house_code_input.send_keys('FA-32')
        self.temperature_opentrv_input.send_keys('23.233\n')
        # # user then waits for the temperature to update
        self.wait_for_attribute_in_cache('FA-32', 'temperature-opentrv', 23.233)
        import time
        # user updates the rest of the variables
        # relative_humidity
        self.relative_humidity_input.send_keys('50\n')
        self.wait_for_attribute_in_cache('FA-32', 'relative-humidity', 50)
        # temperature_ds18b20
        self.temperature_ds18b20_input.send_keys('25.333\n')
        self.wait_for_attribute_in_cache('FA-32', 'temperature-ds18b20', 25.333)
        # window
        self.window_input.send_keys('open')
        self.window_form.submit()
        self.wait_for_attribute_in_cache('FA-32', 'window', 'open')
        # switch
        self.switch_input.send_keys('on')
        self.switch_form.submit()
        self.wait_for_attribute_in_cache('FA-32', 'switch', 'on')
        # last-updated-all
        self.last_updated_all_input.send_keys("2015-07-10\n")
        self.last_updated_all_form.submit()
        self.wait_for_attribute_in_cache('FA-32', 'last-updated-all', '2015-07-10T00:00:00Z')
        # last-updated-temperature
        self.last_updated_temperature_input.send_keys("2015-07-10\n")
        self.last_updated_temperature_form.submit()
        self.wait_for_attribute_in_cache('FA-32', 'last-updated-temperature', '2015-07-10T00:00:00Z')
        # synchronising
        self.synchronising_input.send_keys('on')
        self.synchronising_form.submit()
        self.wait_for_attribute_in_cache('FA-32', 'synchronising', 'on')
        # ambient light
        self.ambient_light_input.send_keys('50\n')
        self.wait_for_attribute_in_cache('FA-32', 'ambient-light', 50)

    def test_switch_switches_off_after_shown_as_on_in_the_cache(self):

        # user goes to the api page and enters a house code
        self.post_house_code('FA-32')
        # user then goes to the rev2 emulator pages to check it's there
        self.initialise_page()
        self.house_code_input.send_keys('FA-32')
        self.switch_input.send_keys('on')
        self.switch_form.submit()
        self.wait_for_attribute_in_cache('FA-32', 'switch', 'on')
        # the next time the cache updates the switch should be off
        self.wait_for_attribute_in_cache('FA-32', 'switch', 'off')
        
    def wait_for_attribute_in_cache(self, code, name, value, timeout=10):

        def check_variable_found(b):
            json_response = b.find_element_by_id("id-cache").text
            if json_response != "":
                json_response = json.loads(json_response)
                for hc in json_response:
                    if hc['house-code'] == code and name in hc:
                            return hc[name] == value
                return False

        timeout_msg = 'Count not find attribute: {} with val: {}'.format(name, value)
        WebDriverWait(self.browser,timeout=timeout).until(check_variable_found, timeout_msg)
