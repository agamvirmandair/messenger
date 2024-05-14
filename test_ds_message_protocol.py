""" This moduleis respnsible for testing ds_message protocol"""
# AGAMVIR SINGH MANDAIR
# mandaira@uci.edu
# 40141643
import unittest
from collections import namedtuple
from ds_protocol import direct_msg


class TestDsmessageProtocol(unittest.TestCase):
    """ Testing dsmessage protocol"""
    def test_direct_msg(self):
        """ function to assert different messages"""
        DataTuple = namedtuple('DataTuple', ['foo', 'baz'])

        assert direct_msg('{"response": {"type": "ok", "messages": \
[{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689\
.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp\
":"1603167689.3928561"}]}}') == DataTuple(foo='ok', baz=[{'message': '\
Hello User 1!', 'from': 'markb', 'timestamp': '1603167689.392856\
1'}, {'message': 'Bzzzzz', 'from': 'thebeemoviescript', 'timestam\
p': '1603167689.3928561'}])

        assert direct_msg('{"response": {"type": "ok", "messages": \
[{"message":"Good morning", "from":"gama", "timestamp": "1403167589.\
3428561"}]}}') == DataTuple(foo='ok', baz=[{'message': 'Good morning\
', 'from': 'gama', 'timestamp': '1403167589.3428561'}])


if __name__ == "__main__":
    unittest.main()
