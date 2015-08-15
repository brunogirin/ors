import time
import datetime
import requests
import api.models
import logging
import django.conf
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class FunctionalTest(StaticLiveServerTestCase):

    pass

class ValveApiTest(FunctionalTest):

    def test_valve_api(self):

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
        # user waits 15 minutes and checks to see the house code object has been updated
        django.conf.settings.POLLING_FREQUENCY = datetime.timedelta(seconds=10)
        time.sleep(django.conf.settings.POLLING_FREQUENCY.seconds + 10)
        response = requests.get(self.live_server_url + '/api/status/FA-32')
        updated_status = response.json()['content']
        self.assertNotEqual(initial_status, updated_status)
