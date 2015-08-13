import mock
import unittest
import rev2
from api.models import HouseCode

class Base(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

class SendPollAndCommandTest(Base):

    @mock.patch('rev2.serial.Serial.readline')
    def test_poll_and_command_timesout_when_there_is_no_response(self, mock_readline):
        mock_readline.return_value = '>' # no response
        rev2_interface = rev2.Rev2Interface()
        poll_and_command = mock.Mock()

        with self.assertRaises(rev2.TimeoutException):
            rev2_interface.send_poll_and_command(poll_and_command)

    @mock.patch('rev2.Rev2Interface.send_and_wait_for_response')
    def test_poll_retries_n_times(self, mock_send_and_wait_for_response):
        def timeout_exception_raise(poll_and_command):
            raise rev2.TimeoutException()
        mock_send_and_wait_for_response.side_effect = timeout_exception_raise
        with self.assertRaises(rev2.TimeoutException):
            rev2.rev2_interface.send_poll_and_command(rev2.PollAndCommand(), retries=3, timeout=1)
        self.assertEqual(mock_send_and_wait_for_response.call_count, 4)

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
        
class UpdateStatusTest(Base):
    
    @mock.patch('rev2.Rev2Interface.send_poll_and_command')
    def test_poll_for_status_updates_housecode_object(self, mock_send_poll_and_command):

        poll_response = mock.Mock()
        poll_response.relative_humidity = mock.Mock(return_value=50)
        poll_response.temperature_ds18b20 = mock.Mock(return_value=20)
        mock_send_poll_and_command.return_value = poll_response
        house_code = mock.Mock()
        house_code.code = 'FA-32'
        house_code.save = mock.Mock()
        def changes_saved():
            self.assertEqual(house_code.relative_humidity, 50)
            self.assertEqual(house_code.temperature_ds18b20, 20)
        house_code.save.side_effect = changes_saved

        rev2_interface = rev2.Rev2Interface()
        rev2_interface.update_status(house_code)

        house_code.save.assert_called_once_with()

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
            self.assertEqual(poll_and_command.house_code, house_code.code)
            self.assertEqual(poll_and_command.rad_open_percent, 50)
            self.assertEqual(poll_and_command.light_colour, 2)
            self.assertEqual(poll_and_command.light_on_time, 30)
            self.assertEqual(poll_and_command.light_flash, 1)
            return mock.Mock()
            
        mock_send_poll_and_command.return_value = mock.Mock()
        mock_send_poll_and_command.side_effect = check_poll_and_command

        rev2_interface = rev2.Rev2Interface()
        rev2_interface.update_status(house_code)

