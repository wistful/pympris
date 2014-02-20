#!/usr/bin/env python
# coding=utf-8

# Copyright (c) Mikhail Mamrouski.
# See LICENSE for details.

"""
This module provides a `Base` class used as a base class
for implementing MPRIS2 interfaces.

`BaseMeta` metaclass uses to avoid returning dbus types and exceptions.
"""

from functools import partial

import dbus

from .common import (
    signal_wrapper, filter_properties_signals,
    ExceptionMeta, ConverterMeta,
)

IPROPERTIES = "org.freedesktop.DBus.Properties"


class BaseMeta(ExceptionMeta, ConverterMeta):
    pass

BaseVersionFix = BaseMeta('BaseVersionFix', (object,), {})


class Base(BaseVersionFix):

    """Base class provides common functionality
    for other classes which implement MPRIS2 interfaces"""

    OBJ_PATH = "/org/mpris/MediaPlayer2"

    def __init__(self, name, bus=None, private=False):
        """Init inner attributes to work with dbus.

        :param name: unique or well-known objects name
        :param bus: bus object;
                  new SessionBus() object will be created if value is None.
        :param private: private connection (uses only if bus is None)
        """
        if not bus:
            bus = dbus.SessionBus(private=private)
        self.bus = bus
        """Bus object from the functions argument or SessionBus()"""

        self.name = name
        """objects name from the functions argument"""

        self.proxy = bus.get_object(name, self.OBJ_PATH)
        """DBUS proxy object"""

        self.iface = dbus.Interface(self.proxy, self.IFACE)
        """DBUS interface (uses self.IFACE path to create it)"""

        self.properties = dbus.Interface(self.proxy, IPROPERTIES)
        """DBUS interface to work with object's properties"""

        self.get = partial(self.properties.Get, self.IFACE)
        """function to receive property's value"""

        self.set = partial(self.properties.Set, self.IFACE)
        """function to set property's value"""

    def register_signal_handler(self, signal_name, handler_function):
        """register `handler_function` to receive `signal_name`.

        Uses class's dbus interface self.IFACE, objects name self.name
        and objects path self.OBJ_PATH to match signal.
        """
        self.bus.add_signal_receiver(signal_wrapper(handler_function),
                                     signal_name=signal_name,
                                     dbus_interface=self.IFACE,
                                     bus_name=self.name,
                                     path=self.OBJ_PATH)

    def register_properties_handler(self, handler_function):
        """register `handler_function` to receive `signal_name`.

        Uses dbus interface IPROPERTIES and objects path self.OBJ_PATH
        to match signal.

        :param handler_function: the function to be called.
        """

        handler = filter_properties_signals(
            signal_wrapper(handler_function), self.IFACE)

        self.bus.add_signal_receiver(handler,
                                     signal_name='PropertiesChanged',
                                     dbus_interface=IPROPERTIES,
                                     bus_name=self.name,
                                     path=self.OBJ_PATH)
