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

        # hc = api.models.HouseCode.objects.get(code='FA-32')
        # print hc.rad_open_percent
        
    def tearDown(self):
        if rev2.rev2_interface.bg_poller:
            rev2.rev2_interface.bg_poller.stop()

            
