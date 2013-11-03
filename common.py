#!/usr/bin/env python
# coding=utf-8
from functools import wraps

import dbus

MPRIS_NAME_PREFIX = "org.mpris.MediaPlayer2"
MPRIS_OBJECT_PATH = "/org/mpris/MediaPlayer2"
IROOT = "org.mpris.MediaPlayer2"
IPLAYER = IROOT + ".Player"
ITRACKLIST = IROOT + ".TrackList"
IPLAYLISTS = IROOT + ".PlayLists"
IPROPERTIES = "org.freedesktop.DBus.Properties"


def convert2dbus(value, signature):
    """Convert Python type to dbus type according signature"""
    type_map = {
        'b': dbus.Boolean, 'y': dbus.Byte, 'n': dbus.Int16,
        'i': dbus.Int32, 'x': dbus.Int64, 'q': dbus.UInt16, 'u': dbus.UInt32,
        't': dbus.UInt64, 'd': dbus.Double, 'o': dbus.ObjectPath,
        'g': dbus.Signature, 's': dbus.UTF8String}
    return type_map[signature](value)


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


def converter(f):
    """Decorator to convert from dbus type to Python type"""
    @wraps(f)
    def wrapper(*args, **kwds):
        return convert(f(*args, **kwds))
    return wrapper


def available_players():
    bus = dbus.SessionBus()
    players = set()
    for name in filter(lambda item: item.startswith(MPRIS_NAME_PREFIX),
                       bus.list_names()):
        owner_name = bus.get_name_owner(name)
        players.add(convert(owner_name))
    return players


print(available_players())
