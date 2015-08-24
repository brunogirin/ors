import subprocess
import re
import time
import datetime
import serial
import mock
import api.models
from django.conf import settings
from abc import ABCMeta
from django.utils import timezone

class PollingPattern:
    pass

class StandardPollingPattern(PollingPattern):
    def __init__(self, house_codes):
        self.house_codes = house_codes
        self.duration = None
        self.frequency = rev2_interface.POLLING_FREQUENCY
        self.start = None

class DebugPollingPattern(PollingPattern):
    def __init__(self, house_code):
        self.house_codes = [house_code]
        self.duration = rev2_interface.DEBUG_DURATION
        self.frequency = rev2_interface.DEBUG_POLLING_FREQUENCY
        self.start = None

class BackgroundPoller:

    PKL_LOCATION = 'temp/bg_poller.pkl'
    
    def __init__(self, house_codes):
        self.process = None
        self.house_codes = house_codes
        self.polling_patterns = [StandardPollingPattern(house_codes=house_codes)]

    def start(self, bg=True):
        if bg == False:
            now = datetime.datetime.now()
            for polling_pattern in self.polling_patterns:
                if polling_pattern.start == None:
                    polling_pattern.start = now
                    polling_pattern.next = polling_pattern.start + polling_pattern.frequency
            while True:
                polling_pattern = self.next()
                now = datetime.datetime.now()
                if polling_pattern.next > now:
                    time.sleep((polling_pattern.next - now).seconds)
                for house_code in polling_pattern.house_codes:
                    rev2_interface.update_status(house_code)
                    house_code.save()
                polling_pattern.next = polling_pattern.next + polling_pattern.frequency
                if polling_pattern.duration:
                    if polling_pattern.next > polling_pattern.start + polling_pattern.duration:
                        self.polling_patterns.remove(polling_pattern)
                        for polling_pattern_ in self.polling_patterns:
                            if isinstance(polling_pattern_, StandardPollingPattern):
                                polling_pattern_.house_codes.extend(polling_pattern.house_codes)
                                break
        else:
            import cPickle
            with open(self.PKL_LOCATION, 'wb') as f:
                cPickle.dump(self, f)
            args = ['python', 'manage.py', 'start_polling']
            self.process = subprocess.Popen(args)
            # args = ['python', 'manage.py', 'start_polling', '{}'.format(frequency.seconds)]
            # args += [hc.code for hc in self.house_codes]
            # self.process = subprocess.Popen(args)

    def next(self):
        next_polling_pattern = None
        for polling_pattern in self.polling_patterns:
            if next_polling_pattern == None or polling_pattern.next < next_polling_pattern.next:
                next_polling_pattern = polling_pattern
        return next_polling_pattern

    def stop(self):
        if self.process:
            self.process.kill()

    def debug(self, house_code):
        self.remove_house_code(house_code)
        polling_pattern = self.create_debug_polling_pattern(house_code)
        self.add_polling_pattern(polling_pattern)
        self.stop()
        self.start()

    def remove_house_code(self, house_code):
        for polling_pattern in self.polling_patterns:
            if house_code in polling_pattern.house_codes:
                polling_pattern.house_codes.remove(house_code)

    def create_debug_polling_pattern(self, house_code):
        polling_pattern = DebugPollingPattern(house_code)
        return polling_pattern

    def add_polling_pattern(self, polling_pattern):
        self.polling_patterns.append(polling_pattern)

class Rev2InterfaceBase:

    DEFAULT_TIMEOUT = 1
    POLLING_FREQUENCY = datetime.timedelta(minutes=15)

    def __init__(self):

        self.connection = self.connect_to_rev2()
        self.bg_poller = None

    # def bg_poller(self):
    #     return self._bg_poller

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

    def restart_bg_poller(self, house_codes=None):
        bg_poller = self.bg_poller
        if bg_poller:
            bg_poller.stop()
        bg_poller = BackgroundPoller(house_codes)
        bg_poller.start()
        self.bg_poller = bg_poller
        return bg_poller


class Rev2PhysicalInterface(Rev2InterfaceBase):

    POLLING_FREQUENCY = datetime.timedelta(minutes=15)
    DEBUG_DURATION = datetime.timedelta(minutes=10)
    DEBUG_POLLING_FREQUENCY = datetime.timedelta(seconds=10)
    DEFAULT_TIMEOUT = datetime.timedelta(seconds=10)

    def connect_to_rev2(self, location='/dev/ttyUSB0', baud=4800):
        return serial.Serial(location, baud)

class Rev2EmulatorInterface(Rev2InterfaceBase):

    EMULATOR_HOUSE_CODES = ['FA-32', '11-11', 'E2-E1', '45-40', '3A-01']
    POLLING_FREQUENCY = datetime.timedelta(seconds=30)
    DEBUG_DURATION = datetime.timedelta(seconds=10)
    DEBUG_POLLING_FREQUENCY = datetime.timedelta(seconds=1)
    DEFAULT_TIMEOUT = datetime.timedelta(seconds=1)
    
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
        self.last_updated_all = timezone.now()
        self.last_updated_temperature = timezone.now()
        self.synchronising = {'true': 'on', 'false': 'off'}[m.group('synchronising')]
        self.ambient_light = int(round(255. / 61 * (int(m.group('ambient_light')) - 1)))
        
if settings.EMULATE_REV2:

    # def poll(house_code):
    #     return None

    Rev2Interface = Rev2EmulatorInterface
else:
    Rev2Interface = Rev2PhysicalInterface

rev2_interface = Rev2Interface()


