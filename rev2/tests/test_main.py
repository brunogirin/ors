import subprocess
import mock
import unittest
import rev2
from api.models import HouseCode

class Base(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

class BackgroundPollerTest(Base):

    @mock.patch('subprocess.Popen')
    def test_start_is_successful(self, mock_subprocess_popen):
        mock_rev2_interface = mock.Mock(POLLING_FREQUENCY=mock.Mock())
        mock_house_codes = house_codes=[mock.Mock()]

        background_poller = rev2.BackgroundPoller(mock_house_codes)
        background_poller.start(frequency=mock_rev2_interface.POLLING_FREQUENCY)
        
        mock_subprocess_popen.assert_called_once_with(['python', 'manage.py', 'start_polling', str(mock_rev2_interface.POLLING_FREQUENCY.seconds)] + [hc.code for hc in mock_house_codes])

    def test_debug(self):
        mock_house_code = mock.Mock(code='FA-32')
        bg_poller = rev2.BackgroundPoller(house_codes=[mock_house_code])
        # removes house code from existing polling patterns
        mock_remove_house_code = mock.Mock()
        bg_poller.remove_house_code = mock_remove_house_code
        # creates a new debug polling pattern
        mock_create_debug_polling_pattern = mock.Mock()
        mock_polling_pattern = mock.Mock()
        mock_create_debug_polling_pattern.return_value = mock_polling_pattern
        bg_poller.create_debug_polling_pattern = mock_create_debug_polling_pattern
        # adds the polling pattern to the bg poller
        mock_add_polling_pattern = mock.Mock()
        bg_poller.add_polling_pattern = mock_add_polling_pattern
        # restarts the bg poller
        mock_stop_bg_poller = mock.Mock()
        mock_start_bg_poller = mock.Mock()
        bg_poller.stop = mock_stop_bg_poller
        bg_poller.start = mock_start_bg_poller
        
        bg_poller.debug(mock_house_code)
        
        mock_remove_house_code.assert_called_once_with(mock_house_code)
        mock_create_debug_polling_pattern.assert_called_once_with(mock_house_code)
        mock_add_polling_pattern.assert_called_once_with(mock_polling_pattern)
        mock_stop_bg_poller.assert_called_once_with()
        mock_start_bg_poller.assert_called_once_with()

    def test_remove_house_code(self):

        mock_house_code = mock.Mock(code='FA-32')
        bg_poller = rev2.BackgroundPoller(house_codes=[mock_house_code])

        bg_poller.remove_house_code(mock_house_code)

        self.assertNotIn(mock_house_code, bg_poller.polling_patterns[0].house_codes)

    @mock.patch('rev2.DebugPollingPattern')
    def test_create_debug_polling_pattern(self, mock_DebugPollingPattern):

        mock_house_code = mock.Mock(code='FA-32')
        bg_poller = rev2.BackgroundPoller(house_codes=[mock_house_code])
        mock_debug_polling_pattern = mock.Mock()
        mock_DebugPollingPattern.return_value = mock_debug_polling_pattern
        polling_pattern = bg_poller.create_debug_polling_pattern(mock_house_code)
        self.assertEqual(mock_debug_polling_pattern, polling_pattern)

    def test_add_polling_pattern(self):

        mock_polling_pattern = mock.Mock()
        bg_poller = rev2.BackgroundPoller(house_codes=[])
        bg_poller.add_polling_pattern(mock_polling_pattern)
        self.assertEqual(bg_poller.polling_patterns[1], mock_polling_pattern)
    
class PollResponseTest(Base):

    def test_main(self):

        poll_response = rev2.PollResponse("'*' FA-32 FA-32 true|true|1+15 1+100 1+100 true|10|0 nzcrc")
        self.assertEqual(poll_response.house_code, 'FA-32')
        self.assertEqual(poll_response.window, 'open')
        self.assertEqual(poll_response.switch, 'on')
        self.assertEqual(poll_response.relative_humidity, 30)
        self.assertEqual(poll_response.temperature_ds18b20, 50)
        self.assertEqual(poll_response.temperature_opentrv, 25)
        self.assertEqual(poll_response.synchronising, 'on')
        self.assertEqual(poll_response.ambient_light, 38)

class RandomPollResponseGeneratorTest(Base):

    @mock.patch('api.models.HouseCode.generate_random_house_code')
    @mock.patch('rev2.PollResponse')
    def test_generates_a_random_house_code_if_not_given_one(self, mock_poll_response, mock_house_code_generator):

        mock_house_code_generator.return_value = 'FA-32'
        poll_response = mock.Mock()
        mock_poll_response.return_value = poll_response
        
        output = rev2.Rev2EmulatorInterface().generate_random_poll_response(house_code=None)

        self.assertEqual(output, poll_response)
        mock_house_code_generator.assert_called_once_with()
        
class PollAndCommandTest(Base):

    def test_poll_and_command_initialises_correctly(self):

        poll_and_command = rev2.PollAndCommand()
        poll_and_command.command = '?'
        poll_and_command.house_code = 'FA-32'
        poll_and_command.rad_open_percent = 50
        poll_and_command.light_colour = 2
        poll_and_command.light_on_time =  30
        poll_and_command.light_flash =  1

        self.assertEqual(poll_and_command.__str__(), "'?' FA-32 FA-32 1+50 1|1|2 1 1 nzcrc")
        

