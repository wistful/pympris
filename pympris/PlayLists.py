#!/usr/bin/env python
# coding=utf-8

# Copyright (c) Mikhail Mamrouski.
# See LICENSE for details.

"""
Module provides a `PlayLists` class wich implemented MPRIS2 PlayLists interface:
http://specifications.freedesktop.org/mpris-spec/latest/Playlists_Interface.html

Class `PlaylistOrdering` uses as an enum for Ordering type.

Usage::
    from pympris import PlayLists

    pl = PlayLists('org.mpris.MediaPlayer2.rhythmbox')
    print(pl.PlaylistCount)
    print(pl.ActivePlaylist)

    items = pl.GetPlaylists(0, 100, PlaylistOrdering.Alphabetical, reversed=False)
    for uri, name, icon_uri in items:
        print(uri, name, icon_uri)
"""

from .common import convert2dbus
from .Base import Base

__all__ = ('PlayLists', 'PlaylistOrdering', )


class PlaylistOrdering(object):
    Alphabetical = 'Alphabetical'
    CreationDate = 'Created'
    ModifiedDate = 'Modified'
    LastPlayDate = 'Played'
    UserDefined = 'User'


class PlayLists(Base):

    """Class implements methods and properties
    to work with MPRIS2 Playlists interface.
    """

    IFACE = "org.mpris.MediaPlayer2.Playlists"
    """The D-Bus MediaPlayer2.Playlists interface name"""

    def __init__(self, name, bus=None, private=False, obj_path=None):
        super(PlayLists, self).__init__(name=name, bus=bus, private=private, obj_path=obj_path)

    def ActivatePlaylist(self, playlist_id):
        """Starts playing the given playlist.

        :param: str playlist_id: The id of the playlist to activate.
        """
        self.iface.ActivatePlaylist(playlist_id)

    def GetPlaylists(self, start, max_count, order, reversed):
        """Gets a set of playlists.

        :param int start: The index of the first playlist to be fetched
                           (according to the ordering).
        :param int max_count: The maximum number of playlists to fetch.
        :param str order: The ordering that should be used.
        :param bool reversed: Whether the order should be reversed.
        """
        cv = convert2dbus
        return self.iface.GetPlaylists(cv(start, 'u'),
                                       cv(max_count, 'u'),
                                       cv(order, 's'),
                                       cv(reversed, 'b'))

    @property
    def PlaylistCount(self):
        """The number of playlists available."""
        return self.get('PlaylistCount')

    @property
    def Orderings(self):
        """The available orderings. At least one must be offered."""
        return self.get('Orderings')

    @property
    def ActivePlaylist(self):
        """The currently-active playlist."""
        valid, info = tuple(self.get('ActivePlaylist'))
        if valid:
            return info
