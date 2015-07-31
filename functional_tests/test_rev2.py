from .base import FunctionalTest

class Rev2TestCase(FunctionalTest):

    def test_user_posts_a_house_code(self):
        
        # user goes to the api homepage
        self.browser.get(self.server_url)

        # user connects to the usb serial tty
        
        # user connects the rev2 to the usb cable

        # user sees the rev2 boot messgaes

        # rev2 starts to periodically expose the prompt marked with a '>' character

        # status messages print periodically

        # each status updates the database

        # the changes to the database objects is reflected in the rev2 emulator

        # the user now tries to update the valve opening of house code FA-32

        # this change is reflected in the rev2 emulator as well as from the status messages from the rev2
