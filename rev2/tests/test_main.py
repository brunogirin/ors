import mock
import unittest
import rev2
from api.models import HouseCode

class Base(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

class RestartBGPollersTest(Base):

    def test_stops_existing_bg_poller(self):

        bg_poller = mock.Mock(stop=mock.Mock())
        rev2.rev2_interface.bg_poller = bg_poller

        rev2.rev2_interface.restart_bg_poller(house_codes=mock.Mock())

        bg_poller.stop.assert_called_once_with()
    
    def test_stops_existing_bg_poller(self):
        bg_poller = mock.Mock()
        bg_poller.stop = mock.Mock()
        rev2.rev2_interface.bg_poller = bg_poller
        
        rev2.rev2_interface.restart_bg_poller(house_codes=mock.Mock())

        bg_poller.stop.assert_called_once_with()

    def test_no_existing_bg_poller(self):
        bg_poller = None
        rev2.rev2_interface.bg_poller = bg_poller
        
        rev2.rev2_interface.restart_bg_poller(house_codes=mock.Mock())

        # no exception thrown

    @mock.patch('rev2.BackgroundPoller')
    def test_new_bg_poller_returned(self, mock_bg_poller):

        bg_poller = mock.Mock()
        mock_bg_poller.return_value = bg_poller

        self.assertEqual(bg_poller, rev2.rev2_interface.restart_bg_poller(house_codes=mock.Mock()))

    @mock.patch('rev2.BackgroundPoller')
    def test_starts_the_bg_poller(self, mock_bg_poller):

        bg_poller = mock.Mock()
        bg_poller.start = mock.Mock()
        mock_bg_poller.return_value = bg_poller

        rev2.rev2_interface.restart_bg_poller(house_codes=mock.Mock())

        bg_poller.start.assert_called_once_with()

    @mock.patch('rev2.BackgroundPoller')
    def test_rev2_interface_updates_its_bg_poller(self, mock_bg_poller):
        old_bg_poller = mock.Mock()
        rev2.rev2_interface.bg_poller = old_bg_poller
        new_bg_poller = mock.Mock()
        mock_bg_poller.return_value = new_bg_poller

        rev2.rev2_interface.restart_bg_poller(house_codes=mock.Mock())

        self.assertEqual(rev2.rev2_interface.bg_poller, new_bg_poller)
        
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

    # @mock.patch('random.randint')
    # @mock.patch('api.models.HouseCode.generate_random_house_code')
    # def test_generated_house_code_is_passed_to_the_poll_response(self, mock_house_code_generator, mock_rand_int):

    #     mock_house_code_generator.return_value = 'FA-32'
    #     mock_rand_int.side_effect = [0, 0, 0, 0, 0, 0, 1]
        
    #     output = rev2.Rev2EmulatorInterface().generate_random_poll_response(house_code=None)
    #     self.assertEqual(output.response, "'*' FA-32 FA-32 true|true|0+15 0+100 0+100 true|1|0 nzcrc")
        
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
        poll_and_command.house_code = valid_house_codes[0]
        mock_poll_response_generator.return_value = mock.Mock()

        output = rev2.Rev2EmulatorInterface().send_and_wait_for_response(poll_and_command)

        self.assertEqual(output, mock_poll_response_generator.return_value)
        mock_poll_response_generator.assert_called_once_with(house_code=valid_house_codes[0])
    
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
        poll_response.relative_humidity = 50
        poll_response.temperature_ds18b20 = 20
        mock_send_poll_and_command.return_value = poll_response
        house_code = mock.Mock()
        house_code.code = 'FA-32'

        rev2_interface = rev2.Rev2Interface()
        rev2_interface.update_status(house_code)

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

