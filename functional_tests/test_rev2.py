import subprocess
import unittest
import mock

class Rev2TestCase(unittest.TestCase):

    def setUp(self, *args, **kwargs):
        super(Rev2TestCase, self).setUp(*args, **kwargs)

    def tearDown(self, *args, **kwargs):
        super(Rev2TestCase, self).tearDown(*args, **kwargs)

    def runTest(self, *args, **kwargs):
        super(Rev2TestCase, self).runTest()

    def test_usb_not_connected(self):

        # user tries to connect to the rev2

        # an error is returned to the user
        
    def test_rev2_boots_on_connect(self):

        # user connects to the usb serial tty
        subprocess.Popen(['python', 'manage.py', 'rev2', 'connect' '/dev/cu.usbserial-FTH9JD2V'], stdout=subprocess.PIPE)
        
        # user connects the rev2 to the usb cable

        # user sees the rev2 boot messgaes

        # rev2 starts to periodically expose the prompt marked with a '>' character

        # status messages print periodically

        # each status updates the database

        # the changes to the database objects is reflected in the rev2 emulator

        # the user now tries to update the valve opening of house code FA-32

        # this change is reflected in the rev2 emulator as well as from the status messages from the rev2

        

if __name__ == '__main__':
    test_case = Rev2TestCase()
    unittest.main()
