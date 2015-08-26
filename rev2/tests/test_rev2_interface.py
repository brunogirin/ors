import mock
import unittest
import rev2
from api.models import HouseCode

class Base(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
        
    

    
@mock.patch('rev2.BackgroundPoller')
class RestartBGPollersTest(Base):

    def test_stops_existing_bg_poller(self, mock_bg_poller):

        bg_poller = mock.Mock(stop=mock.Mock())
        rev2.rev2_interface.bg_poller = bg_poller

        rev2.rev2_interface.restart_bg_poller(house_codes=mock.Mock())

        bg_poller.stop.assert_called_once_with()
    
    def test_stops_existing_bg_poller(self, mock_bg_poller):
        bg_poller = mock.Mock()
        bg_poller.stop = mock.Mock()
        rev2.rev2_interface.bg_poller = bg_poller
        
        rev2.rev2_interface.restart_bg_poller(house_codes=mock.Mock())

        bg_poller.stop.assert_called_once_with()

    def test_no_existing_bg_poller(self, mock_bg_poller):
        bg_poller = None
        rev2.rev2_interface.bg_poller = bg_poller
        
        rev2.rev2_interface.restart_bg_poller(house_codes=mock.Mock())

        # no exception thrown

    def test_new_bg_poller_returned(self, mock_bg_poller):

        bg_poller = mock.Mock()
        mock_bg_poller.return_value = bg_poller

        self.assertEqual(bg_poller, rev2.rev2_interface.restart_bg_poller(house_codes=mock.Mock()))

    def test_starts_the_bg_poller(self, mock_bg_poller):

        bg_poller = mock.Mock()
        bg_poller.start = mock.Mock()
        mock_bg_poller.return_value = bg_poller

        rev2.rev2_interface.restart_bg_poller(house_codes=mock.Mock())

        bg_poller.start.assert_called_once_with()

    def test_rev2_interface_updates_its_bg_poller(self, mock_bg_poller):
        old_bg_poller = mock.Mock()
        rev2.rev2_interface.bg_poller = old_bg_poller
        new_bg_poller = mock.Mock()
        mock_bg_poller.return_value = new_bg_poller

        rev2.rev2_interface.restart_bg_poller(house_codes=mock.Mock())

        self.assertEqual(rev2.rev2_interface.bg_poller, new_bg_poller)
        
class SendAndWaitForResponseTest(Base):

    @mock.patch('rev2.serial.Serial.readline')
    def test_send_and_wait_for_response_timesout_when_there_is_no_response(self, mock_readline):
        mock_readline.return_value = '>' # no response
        rev2_interface = rev2.Rev2Interface()
        poll_and_command = mock.Mock()

        with self.assertRaises(rev2.TimeoutException):
            rev2_interface.send_and_wait_for_response(poll_and_command)

    @mock.patch('rev2.Rev2EmulatorInterface.generate_random_poll_response')
    def test_returns_a_poll_response_if_the_poll_command_is_valid(self, mock_poll_response_generator):

        valid_house_codes = rev2.Rev2EmulatorInterface.EMULATOR_HOUSE_CODES
        poll_and_command = mock.Mock()
        poll_and_command.house_code = mock.Mock(code=valid_house_codes[0])
        mock_poll_response_generator.return_value = mock.Mock()

        output = rev2.Rev2EmulatorInterface().send_and_wait_for_response(poll_and_command)

        self.assertEqual(output, mock_poll_response_generator.return_value)
        mock_poll_response_generator.assert_called_once_with(house_code=poll_and_command.house_code)
    
class SendPollAndCommandTest(Base):

    @mock.patch('rev2.Rev2Interface.send_and_wait_for_response')
    def test_poll_retries_n_times_then_throws_a_timeout_exception(self, mock_send_and_wait_for_response):
        def timeout_exception_raise(poll_and_command, timeout):
            raise rev2.TimeoutException()
        mock_send_and_wait_for_response.side_effect = timeout_exception_raise
        mock_poll_and_command = mock.Mock()
        with self.assertRaises(rev2.TimeoutException):
            rev2.rev2_interface.send_poll_and_command(mock_poll_and_command, retries=3, timeout=1)
        self.assertEqual(mock_send_and_wait_for_response.call_count, 4)

class UpdateStatusTest(Base):
    
    @mock.patch('rev2.Rev2Interface.send_poll_and_command')
    def test_poll_for_status_updates_housecode_object(self, mock_send_poll_and_command):

        house_code = mock.Mock()
        house_code.code = 'FA-32'
        poll_response = mock.Mock()
        poll_response.house_code = house_code
        poll_response.relative_humidity = 50
        poll_response.temperature_ds18b20 = 20
        mock_send_poll_and_command.return_value = poll_response

        rev2_interface = rev2.Rev2Interface()
        rev2_interface.update_status(house_code=house_code)

        self.assertEqual(house_code.relative_humidity, 50)
        self.assertEqual(house_code.temperature_ds18b20, 20)

    @mock.patch('rev2.Rev2Interface.send_poll_and_command')
    def test_update_status_initialises_poll_and_command_object_correctly(self, mock_send_poll_and_command):
        
        house_code = mock.Mock()
        house_code.code = 'FA-32'
        house_code.rad_open_percent = 50
        house_code.light_colour = 2
        house_code.light_on_time = 30
        house_code.light_flash = 1

        def check_poll_and_command(poll_and_command):
            self.assertEqual(poll_and_command.command, '?')
            self.assertEqual(poll_and_command.house_code, house_code)
            self.assertEqual(poll_and_command.rad_open_percent, 50)
            self.assertEqual(poll_and_command.light_colour, 2)
            self.assertEqual(poll_and_command.light_on_time, 30)
            self.assertEqual(poll_and_command.light_flash, 1)
            return mock.Mock()
            
        mock_send_poll_and_command.side_effect = check_poll_and_command

        rev2_interface = rev2.rev2_interface
        rev2_interface.update_status(house_code=house_code)

