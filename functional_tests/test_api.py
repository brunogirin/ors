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
        print 'test valve'

        rev2.POLLING_FREQUENCY = datetime.timedelta(seconds=10)
        
        # user posts a house code
        response = requests.post(self.live_server_url + '/api/house-codes', data={'house-codes': 'FA-32'})
        self.assertEqual(response.json()['status'], 200)
        print response.content
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

        print api.models.HouseCode.objects.all()
        # hc = api.models.HouseCode.objects.get(code='FA-32')
        # print hc.rad_open_percent
        
    def tearDown(self):
        p1 = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(['grep', 'python manage.py start_polling'], stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        output = p2.communicate()[0]
        pid = int(output.split(' ')[0])
        os.kill(pid, signal.SIGTERM)

            
