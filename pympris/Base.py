#!/usr/bin/env python
# coding=utf-8

# Copyright (c) Mikhail Mamrouski.
# See LICENSE for details.

"""
This module provides a `Base` class used as a base class
for implementing MPRIS2 interfaces.

Decorator 'signal_wrapper' used by `Base` class
to convert function's arguments from dbus type to python type.

`BaseMeta` metaclass (inherited ExceptionMeta and ConverterMeta classes)
to avoid returning or raising dbus types and exceptions.
"""

from functools import partial, wraps
import types
import dbus
from .common import convert, converter, exception_wrapper

IPROPERTIES = "org.freedesktop.DBus.Properties"


def signal_wrapper(f):
    """Decorator converts function's arguments from dbus types to python."""
    @wraps(f)
    def wrapper(*args, **kwds):
        args = map(convert, args)
        kwds = {convert(k): convert(v) for k, v in kwds.items()}
        return f(*args, **kwds)
    return wrapper


class ExceptionMeta(type):

    """Metaclass wraps all class' functions and properties
    in `exception_wrapper` decorator to avoid raising dbus exceptions
    """
    def __new__(cls, name, parents, dct):
        fn = exception_wrapper
        for attr_name in dct:
            if isinstance(dct[attr_name], types.FunctionType):
                dct[attr_name] = fn(dct[attr_name])
            elif isinstance(dct[attr_name], property) and dct[attr_name].fget:
                dct[attr_name] = property(
                    fn(dct[attr_name].fget) if dct[attr_name].fget else None,
                    fn(dct[attr_name].fset) if dct[attr_name].fset else None,
                    fn(dct[attr_name].fdel) if dct[attr_name].fdel else None)

        return super(ExceptionMeta, cls).__new__(cls, name, parents, dct)


class ConverterMeta(type):

    """Metaclass wraps all class' functions and properties
    in `converter` decorator to avoid returning dbus types
    """

    def __new__(cls, name, parents, dct):
        for attr_name in dct:
            if isinstance(dct[attr_name], types.FunctionType):
                dct[attr_name] = converter(dct[attr_name])
            elif isinstance(dct[attr_name], property) and dct[attr_name].fget:
                dct[attr_name] = property(converter(dct[attr_name].fget),
                                          dct[attr_name].fset,
                                          dct[attr_name].fdel
                                          )

        return super(ConverterMeta, cls).__new__(cls, name, parents, dct)


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
