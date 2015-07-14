import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from api.views import INVALID_INPUT_STATUS

class ValveTest(FunctionalTest):

    def get_section(self):
        section = self.browser.find_element_by_id("id-valve-section")
        return section

    def get_inputs(self, section):
        open_input = section.find_element_by_css_selector("input#id-open-input")
        max_temp = section.find_element_by_css_selector("input#id-max-temp-input")
        min_temp = section.find_element_by_css_selector("input#id-min-temp-input")
        button = section.find_element_by_css_selector('input[type="submit"]')
        return (open_input, min_temp, max_temp, button)

    def get_json_response(self):
        try:
            json_response = self.browser.find_element_by_tag_name("pre")
        except Exception as e:
            e.msg += '. Page Source : \n{}'.format(self.browser.page_source)
            raise
        json_response = json.loads(json_response.text)
        return json_response

    def test_main(self):
        
        # Open site
        self.browser.get(self.server_url)
        section = self.get_section()
        header = section.find_element_by_tag_name("h2")
        self.assertEqual("POST /api/valve/house-code", header.text)
        (open_input, min_temp, max_temp, button) = self.get_inputs(section)
        open_input.send_keys("50")
        min_temp.send_keys("20")
        max_temp.send_keys("25")
        # the user submits the form
        button.click()
        # TODO: Test the response of the form submission, don't know what the response looks like currently
        self.assertEqual(self.browser.current_url, self.server_url + '/api/valve/house-code')
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], 200)
        
        # form validation
        # empty inputs
        self.browser.get(self.server_url)
        section = self.get_section()
        (open_input, min_temp, max_temp, button) = self.get_inputs(section)
        button.click()
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        errors = json_response['errors']
        self.assertIn("Invalid input for parameter: open_input. Received: , expected: 0-100", errors) # invalid open input
        self.assertIn("Invalid input for parameter: min_temp. Received: , expected: 7-28", errors) # invalid min_temp input
        self.assertIn("Invalid input for parameter: max_temp. Received: , expected: 7-28", errors) # invalid max_temp input

        # open outside range
        self.browser.get(self.server_url)
        section = self.get_section()
        (open_input, min_temp, max_temp, button) = self.get_inputs(section)
        open_input.send_keys("-1")
        min_temp.send_keys("10")
        max_temp.send_keys("20")
        button.click()
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        errors = json_response['errors']
        self.assertIn("Invalid input for parameter: open_input. Received: -1, expected: 0-100", errors) # invalid open input

        self.browser.get(self.server_url)
        section = self.get_section()
        (open_input, min_temp, max_temp, button) = self.get_inputs(section)
        open_input.send_keys("101")
        min_temp.send_keys("10")
        max_temp.send_keys("20")
        button.click()
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        errors = json_response['errors']
        self.assertIn("Invalid input for parameter: open_input. Received: 101, expected: 0-100", errors) # invalid open input

        # min_temp outside range
        self.browser.get(self.server_url)
        section = self.get_section()
        (open_input, min_temp_input, max_temp_input, button) = self.get_inputs(section)
        open_input.send_keys("50")
        min_temp_input.send_keys("6")
        max_temp_input.send_keys("20")
        button.click()
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        errors = json_response['errors']
        self.assertIn("Invalid input for parameter: min_temp. Received: 6, expected: 7-28", errors) # invalid open input

        self.browser.get(self.server_url)
        section = self.get_section()
        (open_input, min_temp_input, max_temp_input, button) = self.get_inputs(section)
        min_temp_input.send_keys("29")
        button.click()
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        errors = json_response['errors']
        self.assertIn("Invalid input for parameter: min_temp. Received: 29, expected: 7-28", errors) # invalid open input

        # max_temp outside range
        self.browser.get(self.server_url)
        section = self.get_section()
        (open_input, min_temp_input, max_temp_input, button) = self.get_inputs(section)
        max_temp_input.send_keys("6")
        button.click()
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        errors = json_response['errors']
        self.assertIn("Invalid input for parameter: max_temp. Received: 6, expected: 7-28", errors) # invalid open input

        self.browser.get(self.server_url)
        section = self.get_section()
        (open_input, min_temp_input, max_temp_input, button) = self.get_inputs(section)
        max_temp_input.send_keys("29")
        button.click()
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        errors = json_response['errors']
        self.assertIn("Invalid input for parameter: max_temp. Received: 29, expected: 7-28", errors) # invalid open input

        # user puts a max_temp greater or equal to the min temp
        self.browser.get(self.server_url)
        section = self.get_section()
        (open_input, min_temp_input, max_temp_input, button) = self.get_inputs(section)
        open_input.send_keys("50")
        min_temp_input.send_keys("20")
        max_temp_input.send_keys("20")
        button.click()
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        errors = json_response['errors']
        self.assertIn("Invalid input for parameter: max_temp. max_temp (20) must be greater than min_temp (20)", errors)

        self.browser.get(self.server_url)
        section = self.get_section()
        (open_input, min_temp_input, max_temp_input, button) = self.get_inputs(section)
        open_input.send_keys("50")
        min_temp_input.send_keys("21")
        max_temp_input.send_keys("20")
        button.click()
        json_response = self.get_json_response()
        self.assertEqual(json_response['status'], INVALID_INPUT_STATUS)
        errors = json_response['errors']
        self.assertIn("Invalid input for parameter: max_temp. max_temp (20) must be greater than min_temp (21)", errors)
    
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
