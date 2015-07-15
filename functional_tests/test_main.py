import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from api.views import INVALID_INPUT_STATUS, VALID_COLOURS, VALID_FLASH

class LedTest(FunctionalTest):
    '''
    colour: colour of the LED
    flash: how many seconds the LED should flash for
    '''
    
    class PostTestParameterSet(object):

        __slots__ = ['inputs', 'expected_errors', 'expected_status_code', 'expected_content']

        class Inputs(object):
            __slots__ = ['colour', 'flash']

        def __init__(self, inputs=None, expected_errors=None, expected_status_code=None, expected_content=None):
            self.inputs = inputs if inputs != None else self.Inputs()
            self.expected_errors = expected_errors
            self.expected_status_code = expected_status_code
            self.expected_content = expected_content

    def run_input_validation_test(self, parameter_set):
        self.initialise_page()
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
        self.colour_input = self.section.find_element_by_css_selector("input#id-colour-input")
        self.flash_input = self.section.find_element_by_css_selector("input#id-flash-input")
        self.button = self.section.find_element_by_css_selector('input[type="submit"]')

    def test_main(self):
        self.initialise_page()
        h2 = self.section.find_element_by_tag_name('h2')
        self.assertEqual(h2.text, 'POST /api/led/house-code')
        
        # user inputs valid input
        x = self.PostTestParameterSet()
        x.inputs.colour = '0'
        x.inputs.flash = '1'
        x.expected_errors = []
        x.expected_status_code = 200
        x.expected_content = None
        self.run_input_validation_test(x)

        # user inputs empty values
        x = self.PostTestParameterSet()
        x.inputs.colour = ''
        x.inputs.flash = ''
        x.expected_errors =  ['Invalid input for parameter: colour. Received: , expected: [0, 1, 2, 3]', 
                              'Invalid input for parameter: flash. Received: , expected: [1, 2, 4, 8, 16]']
        x.expected_status_code = 300
        x.expected_content = None
        self.run_input_validation_test(x)

        # user inputs alphabetic values
        x = self.PostTestParameterSet()
        x.inputs.colour = 'a'
        x.inputs.flash = 'b'
        x.expected_errors =  ['Invalid input for parameter: colour. Received: a, expected: [0, 1, 2, 3]', 
                              'Invalid input for parameter: flash. Received: b, expected: [1, 2, 4, 8, 16]']
        x.expected_status_code = 300
        x.expected_content = None
        self.run_input_validation_test(x)

        # user enters values outside of range
        x = self.PostTestParameterSet()
        x.inputs.colour = '5'
        x.inputs.flash = '3'
        x.expected_errors =  ['Invalid input for parameter: colour. Received: 5, expected: [0, 1, 2, 3]', 
                              'Invalid input for parameter: flash. Received: 3, expected: [1, 2, 4, 8, 16]']
        x.expected_status_code = 300
        x.expected_content = None
        self.run_input_validation_test(x)

class DebugTest(FunctionalTest):

    class PostTestParameterSet(object):

         __slots__ = ['inputs', 'expected_errors', 'expected_status_code', 'expected_content']
         class Inputs(object):
             __slots__ = ['state_input']
         def __init__(self, inputs=None, expected_errors=None, expected_status_code=None, expected_content=None):
             self.inputs = inputs if inputs != None else self.Inputs()
             self.expected_errors = expected_errors
             self.expected_status_code = expected_status_code
             self.expected_content = expected_content

    def run_input_validation_test(self, parameter_set):
         self.initialise_page()
         self.state_input.send_keys(parameter_set.inputs.state_input)
         self.post_button.click()
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
        self.post_section = self.browser.find_element_by_id("id-debug-post-section")
        self.state_input = self.post_section.find_element_by_css_selector("input#id-state-input")
        self.post_button = self.post_section.find_element_by_css_selector('input[type="submit"]')
        self.get_section = self.browser.find_element_by_id('id-debug-get-section')
        self.get_button = self.get_section.find_element_by_css_selector('input[type="submit"]')

    def test_main(self):
        self.initialise_page()
        h2 = self.post_section.find_element_by_tag_name('h2')
        self.assertEqual(h2.text, 'POST /api/debug')
        
        # user inputs valid input
        x = self.PostTestParameterSet()
        x.inputs.state_input = 'on'
        x.expected_errors = []
        x.expected_status_code = 200
        x.expected_content = None
        self.run_input_validation_test(x)

        # user checks input with /api/debug GET
        self.browser.get(self.server_url + '/api/debug')
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], 200)
        self.assertEqual(json_response['content'], 'on')

        # user turns off debugging
        x = self.PostTestParameterSet()
        x.inputs.state_input = 'off'
        x.expected_errors = []
        x.expected_status_code = 200
        x.expected_content = None
        self.run_input_validation_test(x)
        
        # user checks input with /api/debug GET
        self.browser.get(self.server_url + '/api/debug')
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], 200)
        self.assertEqual(json_response['content'], 'off')

        # user enters empty parameter
        x = self.PostTestParameterSet()
        x.inputs.state_input = ''
        x.expected_errors = ['Invalid input for parameter: state. Received: , expected: on/off']
        x.expected_status_code = INVALID_INPUT_STATUS
        x.expected_content = None
        self.run_input_validation_test(x)

        # user checks input with /api/debug GET
        self.browser.get(self.server_url + '/api/debug')
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], 200)
        self.assertEqual(json_response['content'], 'off')

        # user enters invalid parameter
        x = self.PostTestParameterSet()
        x.inputs.state_input = 'ON'
        x.expected_errors = ['Invalid input for parameter: state. Received: ON, expected: on/off']
        x.expected_status_code = INVALID_INPUT_STATUS
        x.expected_content = None
        self.run_input_validation_test(x)

#         self.assertEqual(self.browser.current_url, self.server_url + '/api/valve/house-code')
#         json_response = self.get_json_response()
#         self.assertEqual(json_response['status'], 200)
        
#         # form validation
#         # empty inputs
#         x = self.TestParameterSet()
#         x.inputs.open_input = ''
#         x.inputs.min_temp = ''
#         x.inputs.max_temp = ''
#         x.expected_errors = ['Invalid input for parameter: open_input. Received: , expected: 0-100']
#         x.expected_errors += ['Invalid input for parameter: min_temp. Received: , expected: 7-28']
#         x.expected_errors += ['Invalid input for parameter: max_temp. Received: , expected: 7-28']
#         x.expected_status_code = INVALID_INPUT_STATUS
#         test_parameter_sets = [x]

#         # open outside range - below min
#         x = self.TestParameterSet()
#         x.inputs.open_input = "-1"
#         x.inputs.min_temp = "10"
#         x.inputs.max_temp = "20"
#         x.expected_status_code = INVALID_INPUT_STATUS
#         x.expected_errors = ["Invalid input for parameter: open_input. Received: -1, expected: 0-100"]
#         test_parameter_sets += [x]
#         # open outside range - above max
#         x = self.TestParameterSet()
#         x.inputs.open_input = "101"
#         x.inputs.min_temp = "10"
#         x.inputs.max_temp = "20"
#         x.expected_status_code = INVALID_INPUT_STATUS
#         x.expected_errors = ["Invalid input for parameter: open_input. Received: 101, expected: 0-100"]
#         test_parameter_sets += [x]

class ValveTest(FunctionalTest):

    class TestParameterSet(object):
        __slots__ = ['inputs', 'expected_errors', 'expected_status_code']
        class InputVals(object):
            __slots__ = ['open_input', 'min_temp', 'max_temp']
        def __init__(self, inputs=None, expected_errors=None, expected_status_code=None):
            self.inputs = inputs if inputs != None else self.InputVals()
            self.expected_errors = expected_errors
            self.expected_status_code = expected_status_code

    def run_input_validation_test(self, parameter_set):
        self.initialise_page()
        self.open_input.send_keys(parameter_set.inputs.open_input)
        self.min_temp.send_keys(parameter_set.inputs.min_temp)
        self.max_temp.send_keys(parameter_set.inputs.max_temp)
        self.button.click()
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], parameter_set.expected_status_code)
        errors = json_response['errors']
        for error in parameter_set.expected_errors:
            self.assertIn(error, errors)

    def initialise_page(self):
        self.browser.get(self.server_url)
        self.section = self.browser.find_element_by_id("id-valve-section")
        self.open_input = self.section.find_element_by_css_selector("input#id-open-input")
        self.max_temp = self.section.find_element_by_css_selector("input#id-max-temp-input")
        self.min_temp = self.section.find_element_by_css_selector("input#id-min-temp-input")
        self.button = self.section.find_element_by_css_selector('input[type="submit"]')

    def test_main(self):
        
        self.initialise_page()
        h2 = self.section.find_element_by_tag_name("h2")
        self.assertEqual(h2.text, "POST /api/valve/house-code")

        # user inputs valid input
        self.open_input.send_keys("50")
        self.min_temp.send_keys("20")
        self.max_temp.send_keys("25")
        # the user submits the form
        self.button.click()
        # TODO: Test the response of the form submission, don't know what the response looks like currently
        self.assertEqual(self.browser.current_url, self.server_url + '/api/valve/house-code')
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], 200)
        
        # form validation
        # empty inputs
        x = self.TestParameterSet()
        x.inputs.open_input = ''
        x.inputs.min_temp = ''
        x.inputs.max_temp = ''
        x.expected_errors = ['Invalid input for parameter: open_input. Received: , expected: 0-100']
        x.expected_errors += ['Invalid input for parameter: min_temp. Received: , expected: 7-28']
        x.expected_errors += ['Invalid input for parameter: max_temp. Received: , expected: 7-28']
        x.expected_status_code = INVALID_INPUT_STATUS
        test_parameter_sets = [x]

        # open outside range - below min
        x = self.TestParameterSet()
        x.inputs.open_input = "-1"
        x.inputs.min_temp = "10"
        x.inputs.max_temp = "20"
        x.expected_status_code = INVALID_INPUT_STATUS
        x.expected_errors = ["Invalid input for parameter: open_input. Received: -1, expected: 0-100"]
        test_parameter_sets += [x]
        # open outside range - above max
        x = self.TestParameterSet()
        x.inputs.open_input = "101"
        x.inputs.min_temp = "10"
        x.inputs.max_temp = "20"
        x.expected_status_code = INVALID_INPUT_STATUS
        x.expected_errors = ["Invalid input for parameter: open_input. Received: 101, expected: 0-100"]
        test_parameter_sets += [x]

        # min_temp outside range - below min
        x = self.TestParameterSet()
        x.inputs.open_input = "50"
        x.inputs.min_temp = "6"
        x.inputs.max_temp = "20"
        x.expected_status_code = INVALID_INPUT_STATUS
        x.expected_errors = ["Invalid input for parameter: min_temp. Received: 6, expected: 7-28"]
        test_parameter_sets += [x]
        # min temp outside range - above max
        x = self.TestParameterSet()
        x.inputs.open_input = "50"
        x.inputs.min_temp = "29"
        x.inputs.max_temp = "20"
        x.expected_status_code = INVALID_INPUT_STATUS
        x.expected_errors = ["Invalid input for parameter: min_temp. Received: 29, expected: 7-28"]
        test_parameter_sets += [x]

        # max_temp outside range - below max
        x = self.TestParameterSet()
        x.inputs.open_input = "50"
        x.inputs.min_temp = "10"
        x.inputs.max_temp = "6"
        x.expected_status_code = INVALID_INPUT_STATUS
        x.expected_errors = ["Invalid input for parameter: max_temp. Received: 6, expected: 7-28"]
        test_parameter_sets += [x]
        # max temp outside range - above max
        x = self.TestParameterSet()
        x.inputs.open_input = "50"
        x.inputs.min_temp = "10"
        x.inputs.max_temp = "29"
        x.expected_status_code = INVALID_INPUT_STATUS
        x.expected_errors = ["Invalid input for parameter: max_temp. Received: 29, expected: 7-28"]
        test_parameter_sets += [x]

        # max temp outside range - above max
        x = self.TestParameterSet()
        x.inputs.open_input = "50"
        x.inputs.min_temp = "10"
        x.inputs.max_temp = "29"
        x.expected_status_code = INVALID_INPUT_STATUS
        x.expected_errors = ["Invalid input for parameter: max_temp. Received: 29, expected: 7-28"]
        test_parameter_sets += [x]

        # user puts a max_temp greater or equal to the min temp
        x = self.TestParameterSet()
        x.inputs.open_input = "50"
        x.inputs.min_temp = "20"
        x.inputs.max_temp = "20"
        x.expected_status_code = INVALID_INPUT_STATUS
        x.expected_errors = ["Invalid input for parameter: max_temp. max_temp (20) must be greater than min_temp (20)"]
        test_parameter_sets += [x]

        x = self.TestParameterSet()
        x.inputs.open_input = "50"
        x.inputs.min_temp = "21"
        x.inputs.max_temp = "20"
        x.expected_status_code = INVALID_INPUT_STATUS
        x.expected_errors = ["Invalid input for parameter: max_temp. max_temp (20) must be greater than min_temp (21)"]
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
        input.send_keys("housecode1")
        button.click()
        self.assertTrue(self.browser.current_url.endswith('/api/house-codes'))
        # assert the returned json has status 200
        self.assertIn('"status": 200', self.browser.page_source)
        self.assertIn('"content": ["housecode1"]', self.browser.page_source)

        # user submits a request to get the house codes
        self.browser.get(self.server_url) # returns to homepage
        section = self.browser.find_element_by_id("id-get-house-codes-section")
        button = section.find_element_by_css_selector('input[type="submit"]')
        button.click()
        # assert the returned json has housecode1 in it
        self.assertIn('"content": ["housecode1"]', self.browser.page_source)

        # user tries to post multiply house codes
        self.browser.get(self.server_url)
        (section, input, button) = self.get_post_house_codes_tags()
        self.assertEqual(input.tag_name, 'textarea')
        input.send_keys("housecode2")
        input.send_keys("\n") # multiple entries are separated by new lines
        input.send_keys("housecode3")
        button = section.find_element_by_css_selector('input[type="submit"]')
        button.click()
        # assert housecode1, housecode2 and housecode3 are in the json response
        self.assertIn('"status": 200', self.browser.page_source)
        self.assertIn('"content": ["housecode2", "housecode3"]', self.browser.page_source) # note household1 has been overwritten

        # user passes a list of housecodes with some duplicates
        self.browser.get(self.server_url)
        (section, input, button) = self.get_post_house_codes_tags()
        input.send_keys("housecode1\nhousecode2\nhousecode1")
        button.click()
        self.assertIn('"content": ["housecode1", "housecode2"]', self.browser.page_source)
        self.assertIn('"warnings": ["ignored duplicate: housecode1"]', self.browser.page_source)

        # user passes empty strings as a house_code
        self.browser.get(self.server_url)
        (section, input, button) = self.get_post_house_codes_tags()
        input.send_keys('\n')
        button.click()
        self.assertIn('"content": []', self.browser.page_source)
        self.assertIn('"warnings": ["ignored empty house code(s)"]', self.browser.page_source)

        # TODO: test for valid input returns relevant errors
        # self.fail("finish tests")

    def get_post_house_codes_tags(self):
        section = self.browser.find_element_by_id("id-post-house-codes-section")
        input = section.find_element_by_id("id-house-codes-input")
        button = section.find_element_by_css_selector('input[type="submit"]')
        return (section, input, button)
