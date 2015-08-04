import sys
import serial
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print 'test command'
        print 'serial: {}'.format(serial)
        with serial.Serial('/dev/tty.usbserial-FTH9JD2V', 4800) as ser:
            n_reads = 0
            while ser.isOpen():
                print 'ser: {}'.format(ser)
                # x = ser.read()
                # print 'x: {}'.format(x)
                # s = ser.read(10)
                # print 's: {}'.format(s)
                line = ser.readline()
                print 'line: {}'.format(line)
                n_reads += 1
                print 'n_reads: {}'.format(n_reads)
                sys.stdout.flush()
                # ser.close()
                # print ser
                # print ser.open()
