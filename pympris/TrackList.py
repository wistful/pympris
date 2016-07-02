#!/usr/bin/env python
# coding=utf-8

# Copyright (c) Mikhail Mamrouski.
# See LICENSE for details.

"""
Module provides a `TrackList` class wich implemented MPRIS2 TrackList interface:
http://specifications.freedesktop.org/mpris-spec/latest/Track_List_Interface.html

Usage::

    from pympris import TrackList

    tl = TrackList('org.mpris.MediaPlayer2.vlc')
    print(tl.Tracks)
    tl.RemoveTrack(tl.Tracks[2])

"""

from .common import convert2dbus
from .Base import Base

__all__ = ('TrackList', )


class TrackList(Base):

    """Class implements methods and properties
    to work with MPRIS2 TrackList interface
    """

    IFACE = "org.mpris.MediaPlayer2.TrackList"
    """The D-Bus MediaPlayer2.Player.TrackList interface name"""

    def __init__(self, name, bus=None, private=False, obj_path=None):
        super(TrackList, self).__init__(name=name, bus=bus, private=private, obj_path=obj_path)

    def GetTracksMetadata(self, track_ids):
        """Gets all the metadata available for a set of tracks.

        :param track_ids: list of track ids

        :returns: Metadata of the set of tracks given as input.
        """
        return self.iface.GetTracksMetadata(convert2dbus(track_ids, 'ao'))

    def AddTrack(self, uri, after_track, set_as_current):
        """Adds a URI in the TrackList.

        :param str uri: The uri of the item to add.
        :param str after_track: The identifier of the track
                                after which the new item should be inserted.
        :param bool set_as_current: Whether the newly inserted track
                                    should be considered as the current track.
        """
        self.iface.AddTrack(uri,
                            convert2dbus(after_track, 'o'),
                            convert2dbus(set_as_current, 'b'))

    def RemoveTrack(self, track_id):
        """Removes an item from the TrackList.

        :param str track_id: Identifier of the track to be removed.
        """
        self.iface.RemoveTrack(convert2dbus(track_id, 'o'))

    def GoTo(self, track_id):
        """Skip to the specified TrackId.

        :param str track_id: Identifier of the track to skip to.
        """
        self.iface.GoTo(convert2dbus(track_id, 'o'))

    @property
    def Tracks(self):
        """
        :returns: A list which contains the identifier of each track
                  in the tracklist, in order.
        """
        return self.get('Tracks')

    @property
    def CanEditTracks(self):
        """If false, calling AddTrack or RemoveTrack will have no effect,
        and may raise a NotSupported error.

        :type: bool
        """
        return self.get('CanEditTracks')
