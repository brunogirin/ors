import mock
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

# class CC1AlertResponseTest(FunctionalTest):

#     def test_response_to_cc1alert(self):
#         # user posts a house_code
#         response = requests.post(self.live_server_url + '/api/house-codes', data={'house-codes': 'FA-32'})
#         response = requests.get(self.live_server_url + '/api/status/FA-32')
#         initial_status = response.json()['content']
#         # a bg process is started that reads the rev2 output
#         # the bg process picks up a cc1 alert and responds accordingly
#         # the bg process triggers a call to update the cache
#         mock_read_input = mock.Mock()
#         mock_read_input.side_effect = ["'!' FA-32 FA-32 1 1 1 1 nzcrc"] + [''] * 10000
#         rev2.rev2_interface.read_input = mock_read_input
#         time.sleep(1) # Give time for the status to update
#         response = requests.get(self.live_server_url + '/api/status/FA-32')
#         status = response.json()['content']
#         self.assertNotEqual(initial_status, status)
        
        
