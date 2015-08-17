import datetime
import time
import json
from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from .base import FunctionalTest
from api.views import INVALID_INPUT_STATUS, INVALID_HOUSE_CODE_MSG, INVALID_LED_COLOUR_MSG
from api.views import INVALID_LED_STATE_MSG, INVALID_LED_REPEAT_INTERVAL_MSG
from api.models import HOUSE_CODE_NOT_FOUND_MSG, HouseCode

class StatusTest(FunctionalTest):
    '''
    relative-humidity
    temperature-opentrv
    temperature-ds18b20
    window
    switch
    last-updated-all
    last-updated-temperature
    led
    synchronising
    ambient-light
    house-code
    '''

    maxDiff = None
    
    def initialise_page(self):
        self.browser.get(self.server_url)
        self.section = self.browser.find_element_by_id("id-status-section")
        self.house_code_input = self.section.find_element_by_id("id-house-code-input")
        self.button = self.section.find_element_by_css_selector('input[type="submit"]')

    def test_main(self):
        ''' Add a house code code and get the status of it '''
        self.initialise_page()
        h2 = self.section.find_element_by_tag_name('h2')
        self.assertEqual(h2.text, 'POST /api/status/<house-code>')

        section = self.browser.find_element_by_id("id-post-house-codes-section")
        input = section.find_element_by_id("id-house-codes-input")
        input.send_keys("FA-32")
        button = section.find_element_by_css_selector('input[type="submit"]')
        button.click()

        # user gets the status of the house code entered previously
        self.initialise_page()
        self.house_code_input.send_keys('FA-32')
        self.button.click()
        self.assertEqual(self.browser.current_url, self.server_url + '/api/status/FA-32')
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], 200)

class LedTest(FunctionalTest):
    
    def initialise_page(self):
        self.browser.get(self.server_url)
        self.section = self.browser.find_element_by_id("id-led-section")
        self.form = self.section.find_element_by_tag_name('form')
        self.house_code_input = self.section.find_element_by_css_selector('input#id-house-code-input')
        self.colour_input = self.section.find_element_by_css_selector("input#id-colour-input")
        self.state_input = self.section.find_element_by_id('id-state-input')
        self.repeat_interval_input = self.section.find_element_by_id('id-repeat-interval-input')
        
    def test_main(self):
        # user adds a house code to the database
        self.post_house_code('FA-32')

        # user reloads the api page
        self.initialise_page()
        h2 = self.section.find_element_by_tag_name('h2')
        self.assertEqual(h2.text, 'POST /api/led/<house-code>')
        # user inputs valid input
        self.house_code_input.send_keys('FA-32')
        self.colour_input.send_keys('0')
        self.state_input.send_keys('0')
        self.repeat_interval_input.send_keys('100')
        self.form.submit()
        self.assertEqual(self.browser.current_url, self.server_url + '/api/led/FA-32')
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], 200)
        self.assertEqual(json_response['content'], None)
        
        # TODO: User needs to be able to see the result
        # Currently the LED post does not affect the cache and is just a dummy function

        # user reloads api page
        # user inputs non existent house code
        self.initialise_page()
        self.house_code_input.send_keys('FA-33')
        self.form.submit()
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(json_response['errors'], [HOUSE_CODE_NOT_FOUND_MSG.format('FA-33')])

        # user inputs empty string for the colour
        self.initialise_page()
        self.house_code_input.send_keys('FA-32')
        self.form.submit()
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertIn(INVALID_LED_COLOUR_MSG.format(''), json_response['errors'])
        self.assertIn(INVALID_LED_STATE_MSG.format(''), json_response['errors'])
        self.assertIn(INVALID_LED_REPEAT_INTERVAL_MSG.format(''), json_response['errors'])

class DebugTest(FunctionalTest):

    def initialise_page(self):
        self.browser.get(self.server_url)
        self.section = self.browser.find_element_by_id('id-debug-section')
        self.form = self.section.find_element_by_tag_name('form')
        self.house_code_input = self.section.find_element_by_id('id-house-code-input')
        self.button = self.form.find_element_by_css_selector('input[type="submit"]')

    def test_main(self):
        # user inputs a house code into the database
        self.post_house_code('FA-32')

        # user reloads the api page
        self.initialise_page()
        h2 = self.section.find_element_by_tag_name('h2')
        self.assertEqual(h2.text, '/api/debug/<house code>')

        # user turns on the debugging
        self.house_code_input.send_keys('FA-32')
        self.form.submit()
        self.assertEqual(self.browser.current_url, self.server_url + '/api/debug/FA-32')

        # user provides a house code that doesn't exist
        self.initialise_page()
        self.form.submit()
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        self.assertEqual(json_response['errors'], [HOUSE_CODE_NOT_FOUND_MSG.format('')])
        
        # TODO: User needs to be able to see the changes from turning debug mode on
        
class ValveTest(FunctionalTest):

    class TestParameterSet(object):
        __slots__ = ['inputs', 'expected_errors', 'expected_status_code']
        class InputVals(object):
            __slots__ = ['open_input', 'min_temp', 'max_temp', 'house_code']
        def __init__(self, inputs=None, expected_errors=None, expected_status_code=None):
            self.inputs = inputs if inputs != None else self.InputVals()
            self.expected_errors = expected_errors
            self.expected_status_code = expected_status_code

    def run_input_validation_test(self, parameter_set):
        self.initialise_page()
        self.house_code_input.send_keys(parameter_set.inputs.house_code)
        self.open_input.send_keys(parameter_set.inputs.open_input)
        self.form.submit()
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], parameter_set.expected_status_code)
        errors = json_response['errors']
        for error in parameter_set.expected_errors:
            self.assertIn(error, errors)

    def initialise_page(self):
        self.browser.get(self.server_url)
        self.section = self.browser.find_element_by_id("id-valve-section")
        self.house_code_input = self.section.find_element_by_css_selector("input#id-house-code-input")
        self.open_input = self.section.find_element_by_css_selector("input#id-open-input")
        self.form = self.section.find_element_by_tag_name('form')

    def test_main(self):

        self.initialise_page()
        h2 = self.section.find_element_by_tag_name("h2")
        self.assertEqual(h2.text, "POST /api/valve/<house-code>")

        section = self.browser.find_element_by_id("id-post-house-codes-section")
        input = section.find_element_by_id("id-house-codes-input")
        input.send_keys("FA-32\n")

        # user inputs valid input
        self.initialise_page()

        self.house_code_input.send_keys('FA-32')
        self.open_input.send_keys("50")
        self.form.submit()
        self.assertEqual(self.browser.current_url, self.server_url + '/api/valve/FA-32')
        # TODO: Test the response of the form submission, don't know what the response looks like currently
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], 200)

        # user inputs a house-code that has a valid format but does not exist
        self.initialise_page()
        self.house_code_input.send_keys('FA-11')
        self.form.submit()
        response = json.loads(self.browser.find_element_by_tag_name("pre").text)
        self.assertEqual(response['errors'], [HOUSE_CODE_NOT_FOUND_MSG.format('FA-11')])
        
        # form validation

        # invalid house-code
        x = self.TestParameterSet()
        x.inputs.house_code = ''
        x.inputs.open_input = '50'
        x.expected_errors = [HOUSE_CODE_NOT_FOUND_MSG.format('')]
        x.expected_status_code = INVALID_INPUT_STATUS
        self.run_input_validation_test(x)
        x = self.TestParameterSet()
        x.inputs.house_code = 'HOUSECODE'
        x.inputs.open_input = '50'
        x.expected_errors = [HOUSE_CODE_NOT_FOUND_MSG.format('HOUSECODE')]
        x.expected_status_code = INVALID_INPUT_STATUS
        self.run_input_validation_test(x)

        test_parameter_sets = []
        # empty inputs
        x = self.TestParameterSet()
        x.inputs.house_code = 'FA-32'
        x.inputs.open_input = ''
        x.expected_errors = ['Invalid input for parameter: open. Received: , expected: 0-100']
        x.expected_status_code = INVALID_INPUT_STATUS
        test_parameter_sets += [x]

        # open outside range - below min
        x = self.TestParameterSet()
        x.inputs.house_code = 'FA-32'
        x.inputs.open_input = "-1"
        x.expected_status_code = INVALID_INPUT_STATUS
        x.expected_errors = ["Invalid input for parameter: open. Received: -1, expected: 0-100"]
        test_parameter_sets += [x]
        # open outside range - above max
        x = self.TestParameterSet()
        x.inputs.house_code = 'FA-32'
        x.inputs.open_input = "101"
        x.expected_status_code = INVALID_INPUT_STATUS
        x.expected_errors = ["Invalid input for parameter: open. Received: 101, expected: 0-100"]
        test_parameter_sets += [x]

        for parameter_set in test_parameter_sets:
            self.run_input_validation_test(parameter_set)
    
class HouseCodeTest(FunctionalTest):

    # TODO: Write test for posting house codes by using a request with content-type of "application/json"
    # This should pass a json object with has a house-codes attribute which is an array of house code strings

    def test_house_codes(self):
        
        # Open site
        self.browser.get(self.server_url)

        # House codes (GET)
        house_codes_section = self.browser.find_element_by_id("id-get-house-codes-section")
        header = house_codes_section.find_element_by_tag_name("h2")
        button = house_codes_section.find_element_by_css_selector('input[type="submit"]')
        button.click()
        self.assertTrue(self.browser.current_url.endswith('/api/house-codes'))
        # assert the returned json is an empty list
        
        # House codes (POST)
        # user returns to homepage
        self.browser.get(self.server_url)
        (section, input, button) = self.get_post_house_codes_tags()
        header = section.find_element_by_tag_name("h2")
        self.assertEqual(header.text, 'POST /api/house-codes')
        # user inputs a house code into an input field
        input.send_keys("FA-32")
        button.click()
        self.assertTrue(self.browser.current_url.endswith('/api/house-codes'))
        # assert the returned json has status 200
        self.assertIn('"status": 200', self.browser.page_source)
        self.assertIn('"content": ["FA-32"]', self.browser.page_source)

        # user submits a request to get the house codes
        self.browser.get(self.server_url) # returns to homepage
        section = self.browser.find_element_by_id("id-get-house-codes-section")
        button = section.find_element_by_css_selector('input[type="submit"]')
        button.click()
        # assert the returned json has housecode1 in it
        self.assertIn('"content": ["FA-32"]', self.browser.page_source)

        # user tries to post multiply house codes
        self.browser.get(self.server_url)
        (section, input, button) = self.get_post_house_codes_tags()
        self.assertEqual(input.tag_name, 'input')
        self.assertEqual(input.get_attribute('type'), 'text')
        input.send_keys("E2-E1")
        input.send_keys(", ") # multiple entries are separated by commas lines
        input.send_keys("45-40")
        button = section.find_element_by_css_selector('input[type="submit"]')
        button.click()
        # assert housecode1, housecode2 and housecode3 are in the json response
        self.assertIn('"status": 200', self.browser.page_source)
        self.assertIn('"content": ["E2-E1", "45-40"]', self.browser.page_source) # note household1 has been overwritten

        # user tries to post multiply house codes - with some additional white space
        self.browser.get(self.server_url)
        (section, input, button) = self.get_post_house_codes_tags()
        input.send_keys(" E2-E1")
        input.send_keys(",  ") # multiple entries are separated by commas lines
        input.send_keys("45-40")
        input.send_keys(",3A-01")
        button = section.find_element_by_css_selector('input[type="submit"]')
        button.click()
        # assert housecode1, housecode2 and housecode3 are in the json response
        self.assertIn('"status": 200', self.browser.page_source)
        self.assertIn('"content": ["E2-E1", "45-40", "3A-01"]', self.browser.page_source) # note household1 has been overwritten

        # user passes a list of housecodes with some duplicates
        self.browser.implicitly_wait(1)
        self.browser.get(self.server_url)
        (section, input, button) = self.get_post_house_codes_tags()
        input.send_keys("FA-32,E2-E1,FA-32")
        button.click()
        self.assertIn('"content": ["FA-32", "E2-E1"]', self.browser.page_source)
        self.assertIn('"warnings": ["ignored duplicate: FA-32"]', self.browser.page_source)

        # user passes empty strings as a house_code
        self.browser.get(self.server_url)
        (section, input, button) = self.get_post_house_codes_tags()
        input.send_keys('')
        button.click()
        self.assertIn('"content": []', self.browser.page_source)
        response = json.loads(self.browser.find_element_by_tag_name("pre").text)
        self.assertIn("This field cannot be blank.", response['errors'])

        # user enters an invalid format for the house code
        self.browser.get(self.server_url)
        (section, input, button) = self.get_post_house_codes_tags()
        input.send_keys('WX-YZ')
        button.click()
        json_response = json.loads(self.browser.find_element_by_tag_name("pre").text)
        self.assertIn('"content": []', self.browser.page_source)
        self.assertEqual(json_response['errors'], ['Invalid input for "house-code". Recieved: WX-YZ, expected XX-XX where XX are uppercase hex numbers'])

        # user enters the same house code twice, api should overwrite
        self.browser.get(self.server_url)
        (section, input, button) = self.get_post_house_codes_tags()
        input.send_keys('FA-32')
        button.click()
        self.browser.get(self.server_url)
        (section, input, button) = self.get_post_house_codes_tags()
        input.send_keys('FA-32')
        button.click()
        self.assertIn('"status": 200', self.browser.page_source)
        self.assertIn('"content": ["FA-32"]', self.browser.page_source)

    def get_post_house_codes_tags(self):
        section = self.browser.find_element_by_id("id-post-house-codes-section")
        input = section.find_element_by_id("id-house-codes-input")
        button = section.find_element_by_css_selector('input[type="submit"]')
        return (section, input, button)

