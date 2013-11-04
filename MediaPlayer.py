#!/usr/bin/env python
# coding=utf-8

from Root import Root
from Player import Player
from PlayLists import PlayLists
from TrackList import TrackList


class MediaPlayer(object):

    """docstring for MediaPlayer"""

    def __init__(self, dbus_name, bus=None):
        super(MediaPlayer, self).__init__()
        self.dbus_name = dbus_name
        self.bus = bus
        self.root = Root(dbus_name, bus)
        self.player = Player(dbus_name, bus)
        self.playlists = PlayLists(dbus_name, bus)
        self.track_list = TrackList(dbus_name, bus)
