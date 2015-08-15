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

        background_poller = rev2.BackgroundPoller()
        background_poller.start()
        mock_subprocess_popen.assert_called_once_with(['python', 'manage.py', 'start_polling'])
    
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
        

