#!/usr/bin/env python
# coding=utf-8

# Copyright (c) Mikhail Mamrouski.
# See LICENSE for details.

"""
Module provides helper functions.
"""

import sys
import types
from collections import namedtuple
from functools import wraps, partial

import dbus

__all__ = ('signal_wrapper', 'filter_properties_signals', 'convert2dbus',
           'ExceptionMeta', 'ConverterMeta', )

PY3 = (sys.version_info[0] == 3)
MPRIS_NAME_PREFIX = "org.mpris.MediaPlayer2"


def convert2dbus(value, signature):
    """Converts `value` type from python to dbus according signature.

    :param value: value to convert to dbus object
    :param str signature: dbus type signature.
    :returns: value in dbus type.
    """
    if len(signature) == 2 and signature.startswith('a'):
        return dbus.Array(value, signature=signature[-1])
    dbus_string_type = dbus.String if PY3 else dbus.UTF8String
    type_map = {
        'b': dbus.Boolean, 'y': dbus.Byte, 'n': dbus.Int16,
        'i': dbus.Int32, 'x': dbus.Int64, 'q': dbus.UInt16, 'u': dbus.UInt32,
        't': dbus.UInt64, 'd': dbus.Double, 'o': dbus.ObjectPath,
        'g': dbus.Signature, 's': dbus_string_type}
    return type_map[signature](value)


def convert(dbus_obj):
    """Converts dbus_obj from dbus type to python type.

    :param dbus_obj: dbus object.
    :returns: dbus_obj in python type.
    """
    _isinstance = partial(isinstance, dbus_obj)
    ConvertType = namedtuple('ConvertType', 'pytype dbustypes')

    pyint = ConvertType(int, (dbus.Byte, dbus.Int16, dbus.Int32, dbus.Int64,
                              dbus.UInt16, dbus.UInt32, dbus.UInt64))
    pybool = ConvertType(bool, (dbus.Boolean, ))
    pyfloat = ConvertType(float, (dbus.Double, ))
    pylist = ConvertType(lambda _obj: list(map(convert, dbus_obj)),
                         (dbus.Array, ))
    pytuple = ConvertType(lambda _obj: tuple(map(convert, dbus_obj)),
                          (dbus.Struct, ))
    types_str = (dbus.ObjectPath, dbus.Signature, dbus.String)
    if not PY3:
        types_str += (dbus.UTF8String,)
    pystr = ConvertType(str if PY3 else unicode, types_str)

    pydict = ConvertType(
        lambda _obj: dict(zip(map(convert, dbus_obj.keys()),
                              map(convert, dbus_obj.values())
                              )
                          ),
        (dbus.Dictionary, )
    )

    for conv in (pyint, pybool, pyfloat, pylist, pytuple, pystr, pydict):
        if any(map(_isinstance, conv.dbustypes)):
            return conv.pytype(dbus_obj)
    else:
        return dbus_obj


def converter(f):
    """Decorator to convert value from dbus type to python type."""
    @wraps(f)
    def wrapper(*args, **kwds):
        return convert(f(*args, **kwds))
    return wrapper


def exception_wrapper(f):
    """Decorator to convert dbus exception to pympris exception."""
    @wraps(f)
    def wrapper(*args, **kwds):
        try:
            return f(*args, **kwds)
        except dbus.exceptions.DBusException as err:
            _args = err.args
            raise PyMPRISException(*_args)
    return wrapper


def available_players():
    """Searchs and returns set of unique names of objects
    which implements MPRIS2 interfaces.

    :returns: set of unique names.
    :type: set
    """
    bus = dbus.SessionBus()
    players = set()
    for name in filter(lambda item: item.startswith(MPRIS_NAME_PREFIX),
                       bus.list_names()):
        owner_name = bus.get_name_owner(name)
        players.add(convert(owner_name))
    return players


class PyMPRISException(Exception):

    """Base exceprion class"""

    def __init__(self, *args):
        super(PyMPRISException, self).__init__(*args)


def signal_wrapper(f):
    """Decorator converts function's arguments from dbus types to python."""
    @wraps(f)
    def wrapper(*args, **kwds):
        args = map(convert, args)
        kwds = {convert(k): convert(v) for k, v in kwds.items()}
        return f(*args, **kwds)
    return wrapper


def filter_properties_signals(f, signal_iface_name):
    """Filters signals by iface name.

    :param function f: function to wrap.
    :param str signal_iface_name: interface name.
    """
    @wraps(f)
    def wrapper(iface, changed_props, invalidated_props, *args, **kwargs):
        if iface == signal_iface_name:
            f(changed_props, invalidated_props)

    return wrapper


class ExceptionMeta(type):

    """Metaclass to wrap all class methods and properties
    using `exception_wrapper` decorator to avoid raising dbus exceptions.
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

    """Metaclass to wrap all class methods and properties
    using `converter` decorator to avoid returning dbus types.
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
