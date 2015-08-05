import re
import time
import datetime
import serial
import mock
from django.conf import settings

def connect_to_rev2(location='/dev/ttyUSB0', baud=4800):
    return serial.Serial(location, baud)

def poll(house_code):
    start_time = datetime.datetime.now()
    timeout = datetime.timedelta(seconds=10)
    regex = "'\*' (?P<house_code>[\w\-\d]+) [\w\-\d]+ (?P<window>\w+)\|(?P<switch>\w+)\|1\+(?P<relative_humidity>\d+) 1\+(?P<temperature_ds18b20>\d+) 1\+(?P<temperature_opentrv>\d+) (?P<synchronising>\w+)\|(?P<ambient_light>\d+)\|0 nzcrc"
    rev2_conn = connect_to_rev2()
    # TODO: read to the latest response from the rev2. Maybe rev2_conn.readlines()
    while True:
        line = rev2_conn.readline()
        if line.startswith('>'):
            time.sleep(1.)
            rev2_conn.write('S\n') # TODO: write the poll and poll sequence to trigger a poll response
            break
        if datetime.datetime.now() - start_time > timeout:
            raise Exception('Timeout: No response from REV2, did not see input prompt')
    while True:
        line = rev2_conn.readline()
        if line.startswith("'*'"):
            m = re.search(regex, line)
            house_code_id = m.group('house_code')
            if house_code_id == house_code.code:
                break
        if datetime.datetime.now() - start_time > timeout:
            raise Exception('Timeout: No response from REV2: did not see a poll response')
    house_code.relative_humidity = int(m.group('relative_humidity')) * 2
    house_code.temperature_opentrv = '{:.3f}'.format(float(m.group('temperature_opentrv')) * 0.5)
    house_code.temperature_ds18b20 = '{:.3f}'.format(float(m.group('temperature_ds18b20')) * 0.25)
    house_code.window = {'false': 'closed', 'true': 'open'}[m.group('window')]
    house_code.switch = {'false': 'off', 'true': 'on'}[m.group('switch')]
    house_code.last_updated_all = datetime.datetime.now()
    house_code.last_updated_temperature = datetime.datetime.now()
    house_code.synchronising = {'false': 'off', 'true': 'on'}[m.group('synchronising')]
    house_code.ambient_light = int(round(1 + 1. * 254 / 61 * (int(m.group('ambient_light')) - 1)))
    
if settings.EMULATE_REV2:

    def poll(house_code):
        return None
