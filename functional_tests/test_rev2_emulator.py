import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from api.views import INVALID_INPUT_STATUS, VALID_COLOURS, VALID_FLASH, INVALID_HOUSE_CODE_MSG
from api.models import HOUSE_CODE_NOT_FOUND_MSG, HouseCode

class Rev2EmulatorTest(FunctionalTest):

    def initialise_page(self):
        self.browser.get(self.server_url + '/rev2-emulator')
        self.house_code_input = self.browser.find_element_by_id('id-house-code-input')
        self.room_temp_input = self.browser.find_element_by_id('id-room-temp-input')
        self.submit_button = self.browser.find_element_by_css_selector('input[type="submit"]')

    def test_main(self):
        
        # user adds a house_code via the api web page
        self.post_house_code('FA-32')

        # user checks the page title
        self.initialise_page()
        self.assertEqual(self.browser.title, "REV2 Emulator")
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(h1.text, "REV2 Emulator")

        # user enters a new temperature
        self.house_code_input.send_keys('FA-32')
        self.room_temp_input.send_keys('23.125')
        self.submit_button.click()
        self.assertEqual(self.browser.current_url, self.server_url + '/')

        # user checks the change has had an effect in the api web page
        self.get_status('FA-32')
        json_response = self.get_json_response()
        self.assertEqual(json_response['content']['temperature-opentrv'], '23.125')

        # user tries again to enter a new temperature
        self.initialise_page()
        self.house_code_input.send_keys('FA-32')
        self.room_temp_input.send_keys('15.122')
        self.submit_button.click()
        self.assertEqual(self.browser.current_url, self.server_url + '/')

        # user checks the change has had an effect in the api web page
        self.get_status('FA-32')
        json_response = self.get_json_response()
        self.assertEqual(json_response['content']['temperature-opentrv'], '15.122')

        # use tries a house-code that does not exist
        self.initialise_page()
        self.house_code_input.send_keys('FA-33')
        self.room_temp_input.send_keys('15.122')
        self.submit_button.click()
        self.assertEqual(self.browser.current_url, self.server_url + '/rev2-emulator/')
