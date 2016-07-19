#!/usr/bin/env python
# coding=utf-8

# Copyright (c) Mikhail Mamrouski.
# See LICENSE for details.

"""
This module provides a `Base` class used as a base class
for implementing MPRIS2 interfaces.
"""

from functools import partial

import dbus

from .common import (
    signal_wrapper, filter_properties_signals,
    ExceptionMeta, ConverterMeta,
)

__all__ = ('Base', )

IPROPERTIES = "org.freedesktop.DBus.Properties"


class BaseMeta(ExceptionMeta, ConverterMeta):
    """
    `BaseMeta` metaclass uses to avoid returning dbus types and exceptions.
    """

BaseVersionFix = BaseMeta('BaseVersionFix', (object,), {})
"""`BaseVersionFix` class uses to support both python2 and python3 versions."""


class Base(BaseVersionFix):

    """`Base` class provides common functionality
    for other classes which implement MPRIS2 interfaces."""

    OBJ_PATH = "/org/mpris/MediaPlayer2"

    def __init__(self, name, bus=None, private=False, obj_path=None):
        """Init inner attributes to work with dbus.

        :param name: unique or well-known objects name
        :param bus: bus object;
                    new SessionBus() object will be created if value is None.
        :param private: if True, create bus object using private connection
                        (uses only if bus is None).
        """
        if not bus:
            bus = dbus.SessionBus(private=private)
        self.bus = bus
        """Bus object from the functions argument or SessionBus()"""

        self.name = name
        """objects name from the functions argument"""

        if not obj_path:
            self.obj_path = self.OBJ_PATH
        else:
            self.obj_path = obj_path

        self.proxy = bus.get_object(name, self.obj_path)
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
        and objects path self.obj_path to match signal.

        :param str signal_name: The signal name;
                                None(default) matches all names.
        :param function handler_function: The function to be called.
        """
        self.bus.add_signal_receiver(signal_wrapper(handler_function),
                                     signal_name=signal_name,
                                     dbus_interface=self.IFACE,
                                     bus_name=self.name,
                                     path=self.obj_path)

    def register_properties_handler(self, handler_function):
        """register `handler_function` to receive `signal_name`.

        Uses dbus interface IPROPERTIES and objects path self.obj_path
        to match 'PropertiesChanged' signal.

        :param function handler_function: The function to be called.
        """

        handler = filter_properties_signals(
            signal_wrapper(handler_function), self.IFACE)

        self.bus.add_signal_receiver(handler,
                                     signal_name='PropertiesChanged',
                                     dbus_interface=IPROPERTIES,
                                     bus_name=self.name,
                                     path=self.obj_path)
