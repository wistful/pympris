#!/usr/bin/env python
# coding=utf-8

"""
http://specifications.freedesktop.org/mpris-spec/latest/Playlists_Interface.html
"""


class PlayLists(object):

    """docstring for PlayLists"""

    def __init__(self, arg):
        super(PlayLists, self).__init__()
        self.arg = arg

    def ActivatePlaylist(self, playlist_id):
        """Starts playing the given playlist.
        Parameters:
            playlist_id - The id of the playlist to activate.
        """

    def GetPlayLists(self, start, max_count, order, reversed):
        """Gets a set of playlists.
        Parameters:
            start - The index of the first playlist to be fetched
                    (according to the ordering).
            max_count - The maximum number of playlists to fetch.
            order - The ordering that should be used.
            reversed - Whether the order should be reversed.

        """

    def PlaylistCount(self):
        """The number of playlists available."""

    def Orderings(self):
        """The available orderings. At least one must be offered."""

    def ActivePlaylist(self):
        """The currently-active playlist."""
