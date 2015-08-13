import json
import requests
import unittest
import mock
import time, datetime
import api.views
from .base import FunctionalTest

class Rev2TestCase(FunctionalTest):

    def test_user_posts_a_house_code(self, mock_poll):

        # user posts a house code 'FA-32'
        response = requests.post(self.server_url + '/api/house-codes', data={'house-codes': 'FA-32'})
        time.sleep(20) # give time for the initialisation of the house code object
        # user gets the status of the house code
        response = requests.get(self.server_url + '/api/status/FA-32')
        response = json.loads(response.content)
        response = response['content']
        # check the house code object attributes have been initialised
        attributes = [
            ('relative-humidity', None),
            ('temperature-opentrv', None),
            ('temperature-ds18b20', None),
            ('window', None),
            ('switch', None),
            ('last-updated-all', None),
            ('last-updated-temperature', None),
            ('synchronising', None),
            ('ambient-light', None),
        ]
        for attribute_name, unintialised_value in attributes:
            self.assertNotEqual(response[attribute_name],
                                uninitialised_value,
                                'attribute_name: {}, value: {}'.format(attribute_name, uninitialised_value)
            )
            
    def test_rev2_is_polled_every_15_minutes(self):

        # user posts a house code 'FA-32'
        response = requests.post(self.server_url + '/api/house-codes', data={'house-codes': 'FA-32'})
        time.sleep(20) # give time for the cache to update
        # user gets the status of the house code
        response = request.get(self.server_url + '/api/status/FA-32')
        response = json.loads(response.content)
        response = response['content']
        last_updated_all = response['last-updated-all']
        next_update_time = last_updated_all + datetime.timedelta(minutes=15)
        seconds_until_next_update = (next_update_time - datetime.now()).seconds
        time.sleep(seconds_until_next_update + 20)
        # compare previous response to current response
        response = request.get(self.server_url + '/api/status/FA-32')
        response = json.loads(response.content)
        response = response['content']
        last_updated_all_2 = response['last-updated-all']
        self.assertNotEqual(last_updated_all, last_updated_all_2)
        # once more
        next_update_time = last_updated_all + datetime.timedelta(minutes=15)
        seconds_until_next_update = (next_update_time - datetime.now()).seconds
        time.sleep(seconds_until_next_updated + 20)
        response = request.get(self.server_url + '/api/status/FA-32')
        response = json.loads(response.content)
        response = response['content']
        last_updated_all_3 = response['last-updated-all']
        self.assertNotEqual(last_updated_all_2, last_updated_all_3)

    @mock.patch('rev2.serial.Serial.readline')
    def test_poll_and_command_retries_when_there_is_no_response(self, mock_readline):
        mock_readline.return_value = '>' # nothing coming back from the REV2

        # user posts a house code 'FA-32'
        response = requests.post(self.server_url + '/api/house-codes', data={'house-codes': 'FA-32'})
        time.sleep(5) # give the cache time to update

        # user sets the valve opening to 50
        # but the rev2 does not response
        response = requests.post(self.server_url + '/api/valve/FA-32', data={'open': 50})
        response = json.loads(response.content)
        self.assertEqual(response['status'], api.views.TIMEOUT_STATUS)

    # @patch('rev2.poll')
    # def test_rev2_is_polled_every_15_minutes(self, mock_poll):
    #     from django.conf import settings
    #     settings.POLLING_FREQUENCY = datetime.timedelta(seconds=15)

    #     # user posts a house code
    #     # a poll is sent to the house code and the cache is updated
    #     def side_effect(house_code):
    #         house_code.relative_humidity = 50
    #     mock_poll.side_effect = side_effect
    #     response = requests.post(self.server_url + '/api/house-codes', data={'house-codes': 'FA-32'})
    #     house_code = HouseCode.objects.get(code='FA-32')
    #     self.assertEqual(house_code.relative_humidity, 50)
    #     mock_poll.assert_called_once_with(house_code)

    #     # the user checks the status of the house code object
    #     response = requests.get(self.server_url + '/api/status/FA-32')
    #     response = json.loads(response.content)
    #     response = response['content']
    #     self.assertEqual(response['relative-humidity'], 50)

    #     # 15 minutes pass and another poll is sent to the house code, the cache is updated
    #     # the user waits 30 seconds just to give the cache time to update
    #     def side_effect(house_code):
    #         house_code.relative_humidity = 51
    #     mock_poll.side_effect = side_effect
    #     time.sleep(datetime.timedelta(seconds=15.5).seconds)
    #     self.assertEqual(house_code.relative_humidity, 51)

    #     # another 15 minutes pass and another poll is sent to the house code, the cache is updated again
    #     # the user waits 30 seconds just to give the cache time to update
    #     def side_effect(house_code):
    #         house_code.relative_humidity = 52
    #     mock_poll.side_effect = side_effect
    #     time.sleep(datetime.timedelta(seconds=15.5).seconds)
    #     self.assertEqual(house_code.relative_humidity, 52)
        
