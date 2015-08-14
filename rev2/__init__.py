import re
import time
import datetime
import serial
import mock
import api.models
from django.conf import settings
from abc import ABCMeta

class Rev2InterfaceBase:

    DEFAULT_TIMEOUT = 1

    def __init__(self):

        self.connection = self.connect_to_rev2()

    def open_valve(self, open):
        pass

    def send_poll_and_command(self, poll_and_command, retries=0, timeout=None):
        timeout = timeout if timeout else self.DEFAULT_TIMEOUT
        
        try:
            return self.send_and_wait_for_response(poll_and_command, timeout=timeout)
        except TimeoutException as e:
            if retries != 0:
                return self.send_poll_and_command(poll_and_command, retries=retries-1, timeout=timeout)
            else:
                raise e

    def update_status(self, house_code):
        poll_and_command = PollAndCommand()
        poll_and_command.command = '?'
        poll_and_command.house_code = house_code.code
        poll_and_command.rad_open_percent = house_code.rad_open_percent
        poll_and_command.light_colour = house_code.light_colour
        poll_and_command.light_on_time = house_code.light_on_time
        poll_and_command.light_flash = house_code.light_flash
        response = self.send_poll_and_command(poll_and_command)
        house_code.relative_humidity = response.relative_humidity
        house_code.temperature_opentrv = response.temperature_opentrv
        house_code.temperature_ds18b20 = response.temperature_ds18b20
        house_code.window = response.window
        house_code.switch = response.switch
        house_code.last_updated_all = response.last_updated_all
        house_code.last_updated_temperature = response.last_updated_temperature
        house_code.synchronising = response.synchronising
        house_code.ambient_light = response.ambient_light

    def send_and_wait_for_response(self, poll_and_command, timeout=None):
        timeout = timeout if timeout else self.DEFAULT_TIMEOUT
        # self.connection.write('S\n')
        # wait for response
        # if no response raise exception
        # raise TimeoutException()
        # return something else
        raise TimeoutException()

class Rev2PhysicalInterface(Rev2InterfaceBase):

    def connect_to_rev2(self, location='/dev/ttyUSB0', baud=4800):
        return serial.Serial(location, baud)

class Rev2EmulatorInterface(Rev2InterfaceBase):

    EMULATOR_HOUSE_CODES = ['FA-32', '11-11', 'E2-E1', '45-40', '3A-01']

    def connect_to_rev2(self, location=None, baud=None):
        return mock.Mock()

    @staticmethod
    def generate_random_poll_response(house_code=None):
        import random
        if house_code == None:
            house_code = api.models.HouseCode.generate_random_house_code()
        window = ['true', 'false'][random.randint(0, 1)]
        switch = ['true', 'false'][random.randint(0, 1)]
        relative_humidity = random.randint(0, 50)
        temperature_ds18b20 = random.randint(0, 199)
        temperature_opentrv = random.randint(0, 199)
        synchronising = ['true', 'false'][random.randint(0, 1)]
        ambient_light = random.randint(1, 62)
        poll_response = "'*' {house_code} {house_code} ".format(house_code=house_code)
        poll_response += "{window}|{switch}|1+{relative_humidity} ".format(window=window, switch=switch, relative_humidity=relative_humidity)
        poll_response += "1+{temperature_ds18b20} ".format(temperature_ds18b20=temperature_ds18b20)
        poll_response += "1+{temperature_opentrv} ".format(temperature_opentrv=temperature_opentrv)
        poll_response += "{synchronising}|{ambient_light}|0 nzcrc".format(ambient_light=ambient_light, synchronising=synchronising)
        poll_response  = PollResponse(poll_response)
        return poll_response

    def send_and_wait_for_response(self, poll_and_command, timeout=Rev2InterfaceBase.DEFAULT_TIMEOUT):
        if poll_and_command.house_code in self.EMULATOR_HOUSE_CODES:
            poll_response = self.generate_random_poll_response(house_code=poll_and_command.house_code)
            return poll_response
        raise TimeoutException()

class TimeoutException(Exception):
    pass

class PollAndCommand:

    def __str__(self):
        output = "'{command}' {house_code} {house_code} 1+{rad_open_percent} {light_flash}|{light_on_time}|{light_colour} 1 1 nzcrc"
        output = output.format(**{'command': self.command,
                                'house_code': self.house_code,
                                'rad_open_percent': self.rad_open_percent,
                                'light_flash': self.light_flash,
                                'light_on_time': self.light_on_time / 30,
                                'light_colour': self.light_colour})
        return output

class PollResponse:

    REGEX = "'\*' (?P<house_code>[\w\-\d]+) [\w\-\d]+ (?P<window>\w+)\|(?P<switch>\w+)\|1\+(?P<relative_humidity>\d+) 1\+(?P<temperature_ds18b20>\d+) 1\+(?P<temperature_opentrv>\d+) (?P<synchronising>\w+)\|(?P<ambient_light>\d+)\|0 nzcrc"

    def __init__(self, response):
        m = re.search(self.REGEX, response)
        self.house_code = m.group('house_code')
        self.relative_humidity = int(m.group('relative_humidity')) * 2
        self.temperature_opentrv = float(m.group('temperature_opentrv')) * 0.25
        self.temperature_ds18b20 = float(m.group('temperature_ds18b20')) * 0.5
        self.window = {'true': 'open', 'false': 'closed'}[m.group('window')]
        self.switch = {'true': 'on', 'false': 'off'}[m.group('switch')]
        self.last_updated_all = datetime.datetime.now()
        self.last_updated_temperature = datetime.datetime.now()
        self.synchronising = {'true': 'on', 'false': 'off'}[m.group('synchronising')]
        self.ambient_light = int(round(255. / 61 * (int(m.group('ambient_light')) - 1)))
        
# def poll(house_code):
#     start_time = datetime.datetime.now()
#     timeout = datetime.timedelta(seconds=10)
#     regex = "'\*' (?P<house_code>[\w\-\d]+) [\w\-\d]+ (?P<window>\w+)\|(?P<switch>\w+)\|1\+(?P<relative_humidity>\d+) 1\+(?P<temperature_ds18b20>\d+) 1\+(?P<temperature_opentrv>\d+) (?P<synchronising>\w+)\|(?P<ambient_light>\d+)\|0 nzcrc"
#     rev2_conn = connect_to_rev2()
#     # TODO: read to the latest response from the rev2. Maybe rev2_conn.readlines()
#     while True:
#         line = rev2_conn.readline()
#         if line.startswith('>'):
#             time.sleep(1.)
#             rev2_conn.write('S\n') # TODO: write the poll and poll sequence to trigger a poll response
#             break
#         if datetime.datetime.now() - start_time > timeout:
#             raise Exception('Timeout: No response from REV2, did not see input prompt')
#     while True:
#         line = rev2_conn.readline()
#         if line.startswith("'*'"):
#             m = re.search(regex, line)
#             house_code_id = m.group('house_code')
#             if house_code_id == house_code.code:
#                 break
#         if datetime.datetime.now() - start_time > timeout:
#             raise Exception('Timeout: No response from REV2: did not see a poll response')
#     house_code.relative_humidity = int(m.group('relative_humidity')) * 2
#     house_code.temperature_opentrv = '{:.3f}'.format(float(m.group('temperature_opentrv')) * 0.5)
#     house_code.temperature_ds18b20 = '{:.3f}'.format(float(m.group('temperature_ds18b20')) * 0.25)
#     house_code.window = {'false': 'closed', 'true': 'open'}[m.group('window')]
#     house_code.switch = {'false': 'off', 'true': 'on'}[m.group('switch')]
#     house_code.last_updated_all = datetime.datetime.now()
#     house_code.last_updated_temperature = datetime.datetime.now()
#     house_code.synchronising = {'false': 'off', 'true': 'on'}[m.group('synchronising')]
#     house_code.ambient_light = int(round(1 + 1. * 254 / 61 * (int(m.group('ambient_light')) - 1)))
    
if settings.EMULATE_REV2:

    # def poll(house_code):
    #     return None

    Rev2Interface = Rev2EmulatorInterface
else:
    Rev2Interface = Rev2PhysicalInterface

rev2_interface = Rev2Interface()
