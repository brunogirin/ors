from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
    
class MainTest(FunctionalTest):

    def test_main(self):
        
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
        house_codes_section = self.browser.find_element_by_id("id-post-house-codes-section")
        header = house_codes_section.find_element_by_tag_name("h2")
        self.assertEqual(header.text, 'POST /api/house-codes')
        # user inputs a house code into an input field
        input = house_codes_section.find_element_by_id("id-house-codes-input")
        input.send_keys("housecode1")
        button = house_codes_section.find_element_by_css_selector('input[type="submit"]')
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
        section = self.browser.find_element_by_id("id-post-house-codes-section")
        input = section.find_element_by_id("id-house-codes-input")
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
        section = self.browser.find_element_by_id("id-post-house-codes-section")
        input = section.find_element_by_id("id-house-codes-input")
        input.send_keys("housecode1\nhousecode2\nhousecode1")
        button = section.find_element_by_css_selector('input[type="submit"]')
        button.click()
        self.assertIn('"content": ["housecode1", "housecode2"]', self.browser.page_source)
        self.assertIn('"warnings": ["ignored duplicate: housecode1"]', self.browser.page_source)

        # TODO: test for valid input returns relevant errors
        self.fail("finish tests")
