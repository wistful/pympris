#!/usr/bin/env python
# coding=utf-8

# Copyright (c) Mikhail Mamrouski.
# See LICENSE for details.

"""
This module provides a `PlayLists` class
wich implemented MPRIS2 PlayLists interface:
http://specifications.freedesktop.org/mpris-spec/latest/Playlists_Interface.html

class PlaylistOrdering uses as an enum for Ordering type.

pl = PlayLists('org.mpris.MediaPlayer2.rhythmbox')
print pl.PlaylistCount
print pl.ActivePlaylist

items = pl.GetPlaylists(0, 100, PlaylistOrdering.Alphabetical, reversed=False)
for uri, name, icon_uri in items:
    print uri, name, icon_uri
"""

from common import converter, convert2dbus
from Base import Base


class PlaylistOrdering(object):
    Alphabetical = 'Alphabetical'
    CreationDate = 'Created'
    ModifiedDate = 'Modified'
    LastPlayDate = 'Played'
    UserDefined = 'User'


class PlayLists(Base):

    """class implements methods and properties
    to working with MPRIS2 Playlists interface
    """

    IFACE = "org.mpris.MediaPlayer2.Playlists"

    def __init__(self, name, bus=None):
        super(PlayLists, self).__init__(name, bus)

    def ActivatePlaylist(self, playlist_id):
        """Starts playing the given playlist.
        Parameters:
            playlist_id - The id of the playlist to activate.
        """
        self.iface.ActivatePlaylist(playlist_id)

    @converter
    def GetPlaylists(self, start, max_count, order, reversed):
        """Gets a set of playlists.
        Parameters:
            start - The index of the first playlist to be fetched
                    (according to the ordering).
            max_count - The maximum number of playlists to fetch.
            order - The ordering that should be used.
            reversed - Whether the order should be reversed.

        """
        cv = convert2dbus
        return self.iface.GetPlaylists(cv(start, 'u'),
                                       cv(max_count, 'u'),
                                       cv(order, 's'),
                                       cv(reversed, 'b'))

    @property
    @converter
    def PlaylistCount(self):
        """The number of playlists available."""
        return self.get('PlaylistCount')

    @property
    @converter
    def Orderings(self):
        """The available orderings. At least one must be offered."""
        return self.get('Orderings')

    @property
    @converter
    def ActivePlaylist(self):
        """The currently-active playlist."""
        valid, info = tuple(self.get('ActivePlaylist'))
        if valid:
            return info
