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
        self.room_temp_send_button = self.browser.find_element_by_id('id-room-temp-send-button')
        self.ds18b20_temp_input = self.browser.find_element_by_id('id-db18b20-temp-input')
        self.ds18b20_temp_send_button = self.browser.find_element_by_id('id-db18b20-temp-send-button')
        self.button_input = self.browser.find_element_by_id('id-button-input')
        self.button_send_button = self.browser.find_element_by_id('id-button-send-button')
        self.led_input = self.browser.find_element_by_id('id-led-input')
        self.led_send_button = self.browser.find_element_by_id('id-led-send-button')
        self.synchronising_input = self.browser.find_element_by_id('id-synchronising-input')
        self.synchronising_send_button = self.browser.find_element_by_id('id-synchronising-send-button')
        self.relative_humidity_input = self.browser.find_element_by_id('id-relative-humidity-input')
        self.relative_humiidty_send_button = self.browser.find_element_by_id('id-relative-humidity-send-button')
        self.window_input = self.browser.find_element_by_id('id-window-input')
        self.window_send_button = self.browser.find_element_by_id('id-window-send-button')
        self.last_updated_input = self.browser.find_element_by_id('id-last-updated-input')
        self.last_updated_send_button = self.browser.find_element_by_id('id-last-updated-send-button')
        self.last_updated_temperatures_input = self.browser.find_element_by_id('id-last-updated-temperatures-input')
        self.last_updated_temperatures_send_button = self.browser.find_element_by_id('id-last-updated-temperatures-send-button')
        self.get_cached_contents_interval_input = self.browser.find_element_by_id('id-get-cached-contents-interval-input')
        self.get_cached_contents_interval_send_button = self.browser.find_element_by_id('id-get-cached-contents-interval-send-button')

    def test_main(self):
        
        # user adds a house_code via the api web page
        self.post_house_code('FA-32')

        # user checks the page title
        self.initialise_page()
        self.assertEqual(self.browser.title, "REV2 Emulator")
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(h1.text, "REV2 Emulator")

        # Javascript tests

#         # user enters a new temperature
#         self.house_code_input.send_keys('FA-32')
#         self.room_temp_input.send_keys('23.125')
#         self.room_temp_send_button.click()
#         self.assertEqual(self.browser.current_url, self.server_url + '/rev2-emulator')

#         # user checks the change has had an effect in the api web page
#         self.get_status('FA-32')
#         json_response = self.get_json_response()
#         self.assertEqual(json_response['content']['temperature-opentrv'], '23.125')

#         # user tries again to enter a new temperature
#         self.initialise_page()
#         self.house_code_input.send_keys('FA-32')
#         self.room_temp_input.send_keys('15.122')
#         self.submit_button.click()
#         self.assertEqual(self.browser.current_url, self.server_url + '/')

#         # user checks the change has had an effect in the api web page
#         self.get_status('FA-32')
#         json_response = self.get_json_response()
#         self.assertEqual(json_response['content']['temperature-opentrv'], '15.122')

#         # use tries a house-code that does not exist
#         self.initialise_page()
#         self.house_code_input.send_keys('FA-33')
#         self.room_temp_input.send_keys('15.122')
#         self.submit_button.click()
#         self.assertEqual(self.browser.current_url, self.server_url + '/rev2-emulator/')
