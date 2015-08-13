import re
import time
import datetime
import serial
import mock
from django.conf import settings
from abc import ABCMeta

class Rev2InterfaceBase:

    def __init__(self):

        self.connection = self.connect_to_rev2()

    def open_valve(self, open):
        pass

    def send_poll_and_command(self, poll_and_command, retries=0, timeout=1):

        try:
            self.send_and_wait_for_response(poll_and_command)
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
        house_code.relative_humidity = response.relative_humidity()
        house_code.temperature_ds18b20 = response.temperature_ds18b20()
        house_code.save()

    def send_and_wait_for_response(self, poll_and_command):
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

    def connect_to_rev2(self, location=None, baud=None):
        return mock.Mock()

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
