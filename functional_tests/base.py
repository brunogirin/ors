import os
import signal
import subprocess
import json
import sys
from django.test import LiveServerTestCase, TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class FunctionalTest(StaticLiveServerTestCase):

    def get_status(self, house_code):
        self.browser.get(self.server_url)
        section = self.browser.find_element_by_id("id-status-section")
        input = section.find_element_by_id("id-house-code-input")
        input.send_keys(house_code)
        button = section.find_element_by_css_selector('input[type="submit"]')
        button.click()

    def post_house_code(self, house_code):
        self.browser.get(self.server_url)
        section = self.browser.find_element_by_id("id-post-house-codes-section")
        input = section.find_element_by_id("id-house-codes-input")
        input.send_keys(house_code)
        button = section.find_element_by_css_selector('input[type="submit"]')
        button.click()

    def get_json_response(self):
        try:
            json_response = self.browser.find_element_by_tag_name("pre")
        except Exception as e:
            e.msg += '. Page Source : \n{}'.format(self.browser.page_source)
            raise
        json_response = json.loads(json_response.text)
        return json_response

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id),
            'Could not find element with id {}. Page text was {}'.format(
                element_id, self.browser.find_element_by_tag_name('body').text
                )
            )

    def wait_to_be_logged_in(self, email):
        self.wait_for_element_with_id('id_logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    def wait_to_be_logged_out(self, email):
        self.wait_for_element_with_id('id_login')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_host = arg.split('=')[1]
                cls.server_url = 'http://' + cls.server_host
                cls.against_staging = True
                return
        super(FunctionalTest, cls).setUpClass()
        cls.against_staging = False
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url: # i.e. a test on the local machine
            super(FunctionalTest, cls).tearDownClass()
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

        output2 = subprocess.check_output(['ps', '-A'])
        print output2

        print 'stop background polling processes'
        p1 = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(['grep', 'python manage.py start_polling'], stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        output = p2.communicate()[0]
        print 'polling processes:', output
        for i in output.split('\n'):
            if i != '' and 'grep' not in i:
                pid = int(i.strip().split(' ')[0])
                os.kill(pid, signal.SIGTERM)
        import time
        time.sleep(1)
        
