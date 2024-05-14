''' This module defines protocols for communication with server'''
# AGAMVIR SINGH MANDAIR
# mandaira@uci.edu
# 40141643
import json
from collections import namedtuple
DataTuple = namedtuple('DataTuple', ['foo', 'baz'])


def extract_json(json_msg: str) -> DataTuple:
    """ protocol for publishing"""
    try:
        json_obj = json.loads(json_msg)
        msg_type = json_obj["response"]["type"]
        message = json_obj['response']['message']
        return DataTuple(msg_type, message)
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return DataTuple('error', 'error')


def direct_msg(json_msg: str) -> DataTuple:
    """protocol for direct messaging"""
    try:
        json_obj = json.loads(json_msg)
        msg_type = json_obj["response"]["type"]
        messages = json_obj["response"]["messages"]
        return DataTuple(msg_type, messages)
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return DataTuple('error', 'error')
