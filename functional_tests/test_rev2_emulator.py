import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from .base import FunctionalTest
from api.views import INVALID_INPUT_STATUS, VALID_COLOURS, VALID_FLASH, INVALID_HOUSE_CODE_MSG
from api.models import HOUSE_CODE_NOT_FOUND_MSG, HouseCode

class Rev2EmulatorTest(FunctionalTest):

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
        self.house_code_input.send_keys('FA-32')
        # user sees the cache after the inputs
        self.assertTrue(self.browser.find_element_by_tag_name("code"))
        # user sees that a default of 4 seconds has been set for the cache refresh rate
        self.assertEqual(self.get_cached_contents_interval_input.get_attribute('value'), '4')
        self.wait_for_attribute_in_cache('house-code', 'FA-32')

    def wait_for_attribute_in_cache(self, name, value, timeout=10):

        def check_variable_found(b):
            json_response = b.find_element_by_tag_name("code").text
            if json_response != "":
                json_response = json.loads(json_response)
                if name in json_response:
                    return json_response[name] == value

        timeout_msg = 'Count not find attribute: {} with val: {}'.format(name, value)
        WebDriverWait(self.browser,timeout=timeout).until(check_variable_found, timeout_msg)
