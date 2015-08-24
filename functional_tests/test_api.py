import os
import signal
import rev2
import unittest
import time
import datetime
import requests
import api.models
import logging
import django.conf
import subprocess
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class FunctionalTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.live_server_url = 'http://localhost:8000'
        super(FunctionalTest, self).__init__(*args, **kwargs)

class HouseCodesTest(FunctionalTest):

    def test_house_codes_api(self):
        
        rev2.POLLING_FREQUENCY = datetime.timedelta(seconds=10)
        
        # user posts a house code
        response = requests.post(self.live_server_url + '/api/house-codes', data={'house-codes': 'FA-32'})
        self.assertEqual(response.json()['status'], 200)
        # user checks it was initialised okay
        response = requests.get(self.live_server_url + '/api/house-codes')
        self.assertIn('FA-32', response.json()['content'])
        # user checks the initialised values of the house code
        response = requests.get(self.live_server_url + '/api/status/FA-32')
        self.assertEqual(response.json()['status'], 200)
        initial_status = response.json()['content']

        # user checks the house code has not updated yet
        time.sleep(5)
        response = requests.get(self.live_server_url + '/api/status/FA-32')
        self.assertEqual(response.json()['status'], 200)
        current_status = response.json()['content']
        self.assertEqual(current_status, initial_status)
        
        # user checks the house code is updated
        time.sleep(10)
        response = requests.get(self.live_server_url + '/api/status/FA-32')
        updated_status = response.json()['content']
        self.assertNotEqual(initial_status, updated_status)
    
        
class ValveApiTest(FunctionalTest):

    def test_valve_api(self):

        rev2.POLLING_FREQUENCY = datetime.timedelta(seconds=10)
        
        # user posts a house code
        response = requests.post(self.live_server_url + '/api/house-codes', data={'house-codes': 'FA-32'})
        self.assertEqual(response.json()['status'], 200)
        # user checks it was initialised okay
        response = requests.get(self.live_server_url + '/api/house-codes')
        self.assertIn('FA-32', response.json()['content'])
        # user checks the initialised values of the house code
        response = requests.get(self.live_server_url + '/api/status/FA-32')
        self.assertEqual(response.json()['status'], 200)
        initial_status = response.json()['content']
        time.sleep(rev2.POLLING_FREQUENCY.seconds + 5)
        response = requests.get(self.live_server_url + '/api/status/FA-32')
        updated_status = response.json()['content']
        self.assertNotEqual(initial_status, updated_status)

class DebuggingApiTest(FunctionalTest):
    
    def test_debugging(self):

        # user posts the house_codes FA-32 and 11-11
        response = requests.post(self.live_server_url + '/api/house-codes', data={'house-codes': 'FA-32, 11-11'})
        # user checks they were initialised okay
        response = requests.get(self.live_server_url + '/api/house-codes')
        self.assertEqual(response.json()['status'], 200)
        self.assertIn('FA-32', response.json()['content'])
        self.assertIn('11-11', response.json()['content'])
        # # user checks the background polling is working (every 10 seconds)
        # response = requests.get(self.live_server_url + '/api/status/FA-32')
        # initial_status = response.json()['content']
        # time.sleep(1)
        # # 1 second in
        # for i in range(3):
        #     time.sleep(rev2.rev2_interface.POLLING_FREQUENCY.seconds)
        #     response = requests.get(self.live_server_url + '/api/status/FA-32')
        #     current_status = response.json()['content']
        #     self.assertNotEqual(current_status, initial_status)
        #     initial_status = current_status

        # 31 seconds in
        # user calls the api debug method on the 11-11 house code
        # the 11-11 house-code should now update every second for 5 seconds,
        # then it should resume its previous behaviour
        # the FA-32 house-code still updates every 5 seconds
        # rev2.rev2_interface.DEBUG_DURATION = datetime.timedelta(seconds=5)
        print 'call debug on 11-11'
        response = requests.post(self.live_server_url + '/api/debug/11-11')
        response = requests.get(self.live_server_url + '/api/status/11-11')
        initial_status = response.json()['content']
        initial_status_fa32 = requests.get(self.live_server_url + '/api/status/FA-32').json()['content']
        time.sleep(0.5)
        # 0.5 seconds in
        for i in range(rev2.rev2_interface.DEBUG_DURATION.seconds):
            time.sleep(rev2.rev2_interface.DEBUG_POLLING_FREQUENCY.seconds)
            response = requests.get(self.live_server_url + '/api/status/11-11')
            current_status = response.json()['content']
            self.assertNotEqual(initial_status, current_status)
            initial_status = current_status
            # FA-32
            response = requests.get(self.live_server_url + '/api/status/FA-32')
            current_status = response.json()['content']
            self.assertEqual(current_status, initial_status_fa32)
        # debug modes finishes at 36 seconds in
        # 5.5 seconds in
        for i in range(4):
            time.sleep(1)
            response = requests.get(self.live_server_url + '/api/status/11-11')
            current_status = response.json()['content']
            self.assertEqual(current_status, initial_status)
        # 9.5 seconds in
        time.sleep(1)
        # 10.5 seconds in, check the update
        response = requests.get(self.live_server_url + '/api/status/11-11')
        current_status = response.json()['content']
        self.assertNotEqual(initial_status, current_status)
        response = requests.get(self.live_server_url + '/api/status/FA-32')
        current_status = response.json()['content']
        self.assertNotEqual(initial_status_fa32, current_status)
        
    def tearDown(self):
        if rev2.rev2_interface.bg_poller:
            rev2.rev2_interface.bg_poller.stop()

            
            
