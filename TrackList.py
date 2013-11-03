#!/usr/bin/env python
# coding=utf-8

"""
http://specifications.freedesktop.org/mpris-spec/latest/Track_List_Interface.html
"""


class TrackList(object):

    """docstring for TrackList"""

    def __init__(self, arg):
        super(TrackList, self).__init__()
        self.arg = arg

    def GetTracksMetadata(self, track_ids):
        """Gets all the metadata available for a set of tracks.
        Parameters:
            track_ids - list of track ids

        Returns:
            Metadata of the set of tracks given as input.
        """

    def AddTrack(self, uri, after_track, set_as_current):
        """Adds a URI in the TrackList.
        Parameters:
            uri — The uri of the item to add.
            after_track — The identifier of the track
                          after which the new item should be inserted.
            set_as_current - Whether the newly inserted track
                             should be considered as the current track.
        """

    def RemoveTrack(self, track_id):
        """Removes an item from the TrackList.
        Parameters:
            track_id - Identifier of the track to be removed.
        """

    def GoTo(self, track_id):
        """Skip to the specified TrackId.
        Parameters:
            track_id - Identifier of the track to skip to.
        """

    def Tracks(self):
        """Returns an list which contains the identifier of each track
        in the tracklist, in order."""

    def CanEditTracks(self):
        """If false, calling AddTrack or RemoveTrack will have no effect,
        and may raise a NotSupported error."""
