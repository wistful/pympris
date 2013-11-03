#!/usr/bin/env python
# coding=utf-8

from Root import Root
from Player import Player
from PlayLists import PlayLists
from TrackList import TrackList


class MediaPlayer(object):

    """docstring for MediaPlayer"""

    def __init__(self, dbus_name):
        super(MediaPlayer, self).__init__()
        self.dbus_name = dbus_name
        self.root = Root(dbus_name)
        self.player = Player(dbus_name)
        self.playlists = PlayLists(dbus_name)
        self.track_list = TrackList(dbus_name)
