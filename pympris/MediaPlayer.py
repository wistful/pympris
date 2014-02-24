#!/usr/bin/env python
# coding=utf-8

# Copyright (c) Mikhail Mamrouski.
# See LICENSE for details.

"""
Module provides a `MediaPlayer` class
wich contains instances of all implementations of MPRIS2 interfaces.

Usage::

    mp = MediaPlayer('org.mpris.MediaPlayer2.rhythmbox')
    print(mp.root.Identity)
    if mp.root.CanRaise:
        mp.root.Raise()

    if mp.player.CanPause and mp.player.CanPlay:
        mp.player.PlayPause()
    if mp.player.CanGoNext:
        mp.player.Next()

    print(mp.track_list.Tracks)
    print(mp.playlists.PlaylistCount)

    if mp.root.CanQuit:
        mp.root.Quit()
"""

from .Root import Root
from .Player import Player
from .PlayLists import PlayLists
from .TrackList import TrackList

__all__ = ('MediaPlayer', )


class MediaPlayer(object):

    """Class implements all MPRIS2 interfaces."""

    def __init__(self, dbus_name, bus=None, private=False):
        super(MediaPlayer, self).__init__()
        self.root = Root(dbus_name, bus, private)
        """Instance of :class:`pympris.Root` class"""

        self.player = Player(dbus_name, bus, private)
        """Instance of :class:`pympris.Player` class"""

        self.playlists = PlayLists(dbus_name, bus, private)
        """Instance of :class:`pympris.PlayLists` class"""

        self.track_list = TrackList(dbus_name, bus, private)
        """Instance of :class:`pympris.TrackList` class"""
