#!/usr/bin/env python
# coding=utf-8

from functools import partial, wraps

import dbus
from common import IPROPERTIES
from common import convert


def signal_wrapper(f):
    """Decorator converts function's arguments from dbus types to python."""
    @wraps(f)
    def wrapper(*args, **kwds):
        args = map(convert, args)
        kwds = {convert(k): convert(v) for k, v in kwds.items()}
        return f(*args, **kwds)
    return wrapper


class Base(object):
    """Base class to implement dbus Interfaces"""

    OBJ_PATH = "/org/mpris/MediaPlayer2"

    def __init__(self, name, bus=None):
        if not bus:
            bus = dbus.SessionBus()
        self.bus = bus
        self.name = name
        self.proxy = bus.get_object(name, self.OBJ_PATH)
        self.iface = dbus.Interface(self.proxy, self.IFACE)
        self.properties = dbus.Interface(self.proxy, IPROPERTIES)
        self.get = partial(self.properties.Get, self.IFACE)
        self.set = partial(self.properties.Set, self.IFACE)

    def register_signal_handler(self, signal_name, handler_function):
        self.bus.add_signal_receiver(signal_wrapper(handler_function),
                                     signal_name=signal_name,
                                     dbus_interface=self.IFACE,
                                     bus_name=self.name,
                                     path=self.OBJ_PATH)
