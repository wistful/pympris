#!/usr/bin/env python
# coding=utf-8

# Copyright (c) Mikhail Mamrouski.
# See LICENSE for details.

"""
This module provides helper functions:

`convert2dbus` - converts from Python type to DBUS type according signature
`convert` - function to convert dbus object to python object.
`converter` - decorator to convert dbus object to python object.
`exception_wrapper` - decorator to convert dbus exception to pympris exception.
`available_players` - function searchs and returns unique names of objects
                      which implemented MPRIS2 interfaces.

"""

import sys
from functools import wraps
import dbus

MPRIS_NAME_PREFIX = "org.mpris.MediaPlayer2"


def convert2dbus(value, signature):
    """Convert Python type to dbus type according signature"""
    if len(signature) == 2 and signature.startswith('a'):
        return dbus.Array(value, signature=signature[-1])
    type_map = {
        'b': dbus.Boolean, 'y': dbus.Byte, 'n': dbus.Int16,
        'i': dbus.Int32, 'x': dbus.Int64, 'q': dbus.UInt16, 'u': dbus.UInt32,
        't': dbus.UInt64, 'd': dbus.Double, 'o': dbus.ObjectPath,
        'g': dbus.Signature, 's': dbus.UTF8String}
    return type_map[signature](value)

if sys.version_info[0] == 2:
    def convert(dbus_obj):
        if isinstance(dbus_obj, dbus.Boolean):
            return bool(dbus_obj)
        if filter(lambda obj_type: isinstance(dbus_obj, obj_type),
                  (dbus.Byte, dbus.Int16, dbus.Int32, dbus.Int64,
                   dbus.UInt16, dbus.UInt32, dbus.UInt64)):
            return int(dbus_obj)
        if isinstance(dbus_obj, dbus.Double):
            return float(dbus_obj)
        if filter(lambda obj_type: isinstance(dbus_obj, obj_type),
                 (dbus.ObjectPath, dbus.Signature, dbus.String, dbus.UTF8String)):
            return unicode(dbus_obj)
        if isinstance(dbus_obj, dbus.Array):
            return map(convert, dbus_obj)
        if isinstance(dbus_obj, dbus.Dictionary):
            return {convert(key): convert(value)
                    for key, value in dbus_obj.items()}
        if isinstance(dbus_obj, dbus.Struct):
            return tuple(map(convert, dbus_obj))
        return dbus_obj
else:
    def convert(dbus_obj):
        if isinstance(dbus_obj, dbus.Boolean):
            return bool(dbus_obj)
        if [obj_type for obj_type in (dbus.Byte, dbus.Int16, dbus.Int32, dbus.Int64,
                dbus.UInt16, dbus.UInt32, dbus.UInt64) if isinstance(dbus_obj, obj_type)]:
            return int(dbus_obj)
        if isinstance(dbus_obj, dbus.Double):
            return float(dbus_obj)
        if [obj_type for obj_type in (dbus.ObjectPath, dbus.Signature,
                dbus.String) if isinstance(dbus_obj, obj_type)]:
            return str(dbus_obj)
        if isinstance(dbus_obj, dbus.Array):
            return list(map(convert, dbus_obj))
        if isinstance(dbus_obj, dbus.Dictionary):
            return {convert(key): convert(value)
                    for key, value in dbus_obj.items()}
        if isinstance(dbus_obj, dbus.Struct):
            return tuple(map(convert, dbus_obj))
        return dbus_obj

def converter(f):
    """Decorator to convert from dbus type to Python type"""
    @wraps(f)
    def wrapper(*args, **kwds):
        return convert(f(*args, **kwds))
    return wrapper


def exception_wrapper(f):
    """Decorator to convert dbus exception to pympris exception"""
    @wraps(f)
    def wrapper(*args, **kwds):
        try:
            return f(*args, **kwds)
        except dbus.exceptions.DBusException as err:
            _args = err.args
            raise PyMPRISException(*_args)
    return wrapper


def available_players():
    """Search and return set of unique names of objects
    which implemented MPRIS2 interfaces."""
    bus = dbus.SessionBus()
    players = set()
    for name in [item for item in bus.list_names() if item.startswith(MPRIS_NAME_PREFIX)]:
        owner_name = bus.get_name_owner(name)
        players.add(convert(owner_name))
    return players


class PyMPRISException(Exception):
    """docstring for PyMPRISException"""
    def __init__(self, *args):
        super(PyMPRISException, self).__init__(*args)
