import datetime
import time
import json
from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from .base import FunctionalTest
from api.views import INVALID_INPUT_STATUS, VALID_COLOURS, VALID_FLASH, INVALID_HOUSE_CODE_MSG
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

        expected_content = OrderedDict()
        expected_content['house-code'] = 'FA-32'
        expected_content['relative-humidity'] = None
        expected_content['temperature-opentrv'] = None
        expected_content['temperature-ds18b20'] = None
        expected_content['window'] = None
        expected_content['switch'] = None
        expected_content['last-updated-all'] = None
        expected_content['last-updated-temperature'] = None
        expected_content['synchronising'] = None
        expected_content['ambient-light'] = None
        self.assertEqual(json_response['status'], 200)
        self.assertEqual(json_response['content'], expected_content)
        
        # # the user updates the temperature-opentrv
        # self.browser.get(self.server_url + '/rev2-emulator')
        # house_code_input = self.browser.find_element_by_id('id-house-code-input')
        # house_code_input.send_keys('FA-32')
        # temperature_opentrv_input = self.browser.find_element_by_id('id-temperature-opentrv-input')
        # temperature_opentrv_input.send_keys('25\n')
        # # the user waits until the change shows in the cache field below
        # def ajax_success(b):
        #     page_source = b.page_source
        #     json_response = b.find_element_by_tag_name("code")
        #     json_response = json.loads(json_response)
        #     json_response['temperature-opentrv'] == '25'
        # WebDriverWait(
        #     self.browser,
        #     timeout=30).until(
        #         ajax_success,
        #         'Could not find element with id {}. Page text was {}'.format(
        #             element_id, self.browser.find_element_by_tag_name('body').text
        #         )
        #     )
        # # the user goes back to the api page
        # self.browser.get(self.server_url)
        # # the user gets the status for the house-code
        # self.initialise_page()
        # self.house_code_input.send_keys('FA-32')
        # self.button.click()
        # json_response = self.get_json_response()
        # self.assertEqual(json_resposne['status'], 200)
        # self.assertEqual(json_response['content']['temperature-opentrv'], '25')

class LedTest(FunctionalTest):
    '''
    colour: colour of the LED
    flash: how many seconds the LED should flash for
    '''
    
    class PostTestParameterSet(object):

        __slots__ = ['inputs', 'expected_errors', 'expected_status_code', 'expected_content']

        class Inputs(object):
            __slots__ = ['colour', 'flash', 'house_code']

        def __init__(self, inputs=None, expected_errors=None, expected_status_code=None, expected_content=None):
            self.inputs = inputs if inputs != None else self.Inputs()
            self.expected_errors = expected_errors
            self.expected_status_code = expected_status_code
            self.expected_content = expected_content

    def run_input_validation_test(self, parameter_set):
        self.initialise_page()
        self.house_code_input.send_keys(parameter_set.inputs.house_code)
        self.colour_input.send_keys(parameter_set.inputs.colour)
        self.flash_input.send_keys(parameter_set.inputs.flash)
        self.button.click()
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], parameter_set.expected_status_code)
        try:
            errors = json_response['errors']
        except KeyError:
            errors = []
        for error in parameter_set.expected_errors:
            self.assertIn(error, errors)
        self.assertEqual(json_response['content'], parameter_set.expected_content)

    def initialise_page(self):
        self.browser.get(self.server_url)
        self.section = self.browser.find_element_by_id("id-led-section")
        self.house_code_input = self.section.find_element_by_css_selector('input#id-house-code-input')
        self.colour_input = self.section.find_element_by_css_selector("input#id-colour-input")
        self.flash_input = self.section.find_element_by_css_selector("input#id-flash-input")
        self.button = self.section.find_element_by_css_selector('input[type="submit"]')

    def test_main(self):
        self.initialise_page()
        h2 = self.section.find_element_by_tag_name('h2')
        self.assertEqual(h2.text, 'POST /api/led/<house-code>')

        section = self.browser.find_element_by_id("id-post-house-codes-section")
        input = section.find_element_by_id("id-house-codes-input")
        input.send_keys("FA-32")
        button = section.find_element_by_css_selector('input[type="submit"]')
        button.click()

        # user inputs valid input
        self.initialise_page()
        
        # user inputs valid input
        x = self.PostTestParameterSet()
        x.inputs.house_code = 'FA-32'
        x.inputs.colour = '0'
        x.inputs.flash = '1'
        x.expected_errors = []
        x.expected_status_code = 200
        x.expected_content = None
        self.run_input_validation_test(x)
        self.assertEqual(self.browser.current_url, self.server_url + '/api/led/FA-32')

        # user inputs non existent house code
        x = self.PostTestParameterSet()
        x.inputs.house_code = 'E2-E1'
        x.inputs.colour = '0'
        x.inputs.flash = '1'
        x.expected_errors = [HOUSE_CODE_NOT_FOUND_MSG.format('E2-E1')]
        x.expected_status_code = INVALID_INPUT_STATUS
        x.expected_content = None
        self.run_input_validation_test(x)

        # user inputs empty values
        x = self.PostTestParameterSet()
        x.inputs.house_code = 'FA-32'
        x.inputs.colour = ''
        x.inputs.flash = ''
        x.expected_errors =  ['Invalid input for parameter: colour. Received: , expected: [0, 1, 2, 3]', 
                              'Invalid input for parameter: flash. Received: , expected: [1, 2, 4, 8, 16]']
        x.expected_status_code = 300
        x.expected_content = None
        self.run_input_validation_test(x)

        # user inputs alphabetic values
        x = self.PostTestParameterSet()
        x.inputs.house_code = 'FA-32'
        x.inputs.colour = 'a'
        x.inputs.flash = 'b'
        x.expected_errors =  ['Invalid input for parameter: colour. Received: a, expected: [0, 1, 2, 3]', 
                              'Invalid input for parameter: flash. Received: b, expected: [1, 2, 4, 8, 16]']
        x.expected_status_code = 300
        x.expected_content = None
        self.run_input_validation_test(x)

        # user enters values outside of range
        x = self.PostTestParameterSet()
        x.inputs.house_code = 'FA-32'
        x.inputs.colour = '5'
        x.inputs.flash = '3'
        x.expected_errors =  ['Invalid input for parameter: colour. Received: 5, expected: [0, 1, 2, 3]', 
                              'Invalid input for parameter: flash. Received: 3, expected: [1, 2, 4, 8, 16]']
        x.expected_status_code = 300
        x.expected_content = None
        self.run_input_validation_test(x)

class DebugTest(FunctionalTest):

    # class PostTestParameterSet(object):

    #      __slots__ = ['inputs', 'expected_errors', 'expected_status_code', 'expected_content']
    #      class Inputs(object):
    #          __slots__ = ['state_input']
    #      def __init__(self, inputs=None, expected_errors=None, expected_status_code=None, expected_content=None):
    #          self.inputs = inputs if inputs != None else self.Inputs()
    #          self.expected_errors = expected_errors
    #          self.expected_status_code = expected_status_code
    #          self.expected_content = expected_content

    # def run_input_validation_test(self, parameter_set):
    #      self.initialise_page()
    #      self.state_input.send_keys(parameter_set.inputs.state_input)
    #      self.post_button.click()
    #      json_response = self.get_json_response()
    #      self.assertEqual(json_response['status'], parameter_set.expected_status_code)
    #      try:
    #          errors = json_response['errors']
    #      except KeyError:
    #          errors = []
    #      for error in parameter_set.expected_errors:
    #          self.assertIn(error, errors)
    #      self.assertEqual(json_response['content'], parameter_set.expected_content)

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
        x.expected_errors = ['Invalid input for parameter: open_input. Received: , expected: 0-100']
        x.expected_status_code = INVALID_INPUT_STATUS
        test_parameter_sets += [x]

        # open outside range - below min
        x = self.TestParameterSet()
        x.inputs.house_code = 'FA-32'
        x.inputs.open_input = "-1"
        x.expected_status_code = INVALID_INPUT_STATUS
        x.expected_errors = ["Invalid input for parameter: open_input. Received: -1, expected: 0-100"]
        test_parameter_sets += [x]
        # open outside range - above max
        x = self.TestParameterSet()
        x.inputs.house_code = 'FA-32'
        x.inputs.open_input = "101"
        x.expected_status_code = INVALID_INPUT_STATUS
        x.expected_errors = ["Invalid input for parameter: open_input. Received: 101, expected: 0-100"]
        test_parameter_sets += [x]

        for parameter_set in test_parameter_sets:
            self.run_input_validation_test(parameter_set)
    
class HouseCodeTest(FunctionalTest):

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

