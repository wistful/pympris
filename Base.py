#!/usr/bin/env python
# coding=utf-8

from functools import partial

import dbus
from common import IPROPERTIES


class Base(object):
    """Base class to implement dbus Interfaces"""
    def __init__(self, name, bus):
        if not bus:
            bus = dbus.SessionBus()
        self.proxy = bus.get_object(name, self.OBJ_PATH)
        self.iface = dbus.Interface(self.proxy, self.IFACE)
        self.properties = dbus.Interface(self.proxy, IPROPERTIES)
        self.get = partial(self.properties.Get, self.IFACE)
        self.set = partial(self.properties.Set, self.IFACE)
