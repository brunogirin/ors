import mock
from mock import patch
import sys
import requests
import json
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class Rev2TestCase(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_host = arg.split('=')[1]
                cls.server_url = 'http://' + cls.server_host
                cls.against_staging = True
                return
        super(Rev2TestCase, cls).setUpClass()
        cls.against_staging = False
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url: # i.e. a test on the local machine
            super(Rev2TestCase, cls).tearDownClass()

    @patch('rev2.ser')
    def test_user_posts_a_house_code(self, mock_ser):

        mock_ser.readline = mock.Mock()
        mock_ser.readline.side_effect = [
            '>',
            "'*' FA-32 FA-32 false|false|1+25 1+100 1+100 false|50|0 nzcrc",
        ]

        # user posts a house code 'FA-32'
        response = requests.post(self.server_url + '/api/house-codes', data={'house-codes': 'FA-32'})
        # user gets the status of the house code
        response = requests.get(self.server_url + '/api/status/FA-32')
        response = json.loads(response.content)
        response = response['content']
        self.assertEqual(response['relative-humidity'], 50)
