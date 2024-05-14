"""This module contains unit tests for ds_messenger"""
# AGAMVIR SINGH MANDAIR
# mandaira@uci.edu
# 40141643
import unittest
from ds_messenger import DirectMessenger, DirectMessage


class TestDirectMessenger(unittest.TestCase):
    """ responsible for tests"""
    def setUp(self):
        """ setup to instantiate directmessenger object"""
        self.messenger = DirectMessenger('168.235.86.101')

    def test_send(self):
        """ tests send funciton"""
        message = "Hello, World!"
        recipient = "test_user"
        result = self.messenger.send(message, recipient)
        assert isinstance(result, bool), "Expected result to be a boolean"

    def test_retrieve_new(self):
        """ tests retrieve new function"""
        messages = self.messenger.retrieve_new()
        for message in messages:
            assert isinstance(message, DirectMessage), "Expected message\
 to be an instance of DirectMessage"

    def test_retrieve_all(self):
        """ tests retirieve all function"""
        messages = self.messenger.retrieve_all()
        for message in messages:
            assert isinstance(message, DirectMessage), "Expected message \
to be an instance of DirectMessage"


if __name__ == "__main__":
    unittest.main()
