#!/usr/bin/env python
# coding=utf-8

"""
http://specifications.freedesktop.org/mpris-spec/latest/Player_Interface.html
"""


class Player(object):

    """docstring for Player"""

    def __init__(self, arg):
        super(Player, self).__init__()
        self.arg = arg

    def Next(self):
        """Skips to the next track in the tracklist."""

    def Previous(self):
        """Skips to the previous track in the tracklist."""

    def Pause(self):
        """Pauses playback."""

    def PlayPause(self):
        """Pauses playback."""

    def Stop(self):
        """Stops playback."""

    def Play(self):
        """Starts or resumes playback."""

    def Seek(self, offset):
        """Seeks forward in the current track
        Parameters
            Offset — The number of microseconds to seek forward.
        A negative value seeks back.
        """

    def SetPosition(self, track_id, position):
        """Sets the current track position in microseconds.
        Parameters
            track_id - The currently playing track's identifier.
            position — Track position in microseconds.
                This must be between 0 and <track_length>.

        If the Position argument is less than 0, do nothing.
        If the Position argument is greater than the track length, do nothing.
        If the CanSeek property is false, this has no effect.
        """

    def OpenUri(self, uri):
        """Opens the Uri given as an argument
        Parameters
            uri - Uri of the track to load.
        Its uri scheme should be an element
        of the org.mpris.MediaPlayer2.SupportedUriSchemes property
        and the mime-type should match one of the elements
        of the org.mpris.MediaPlayer2.SupportedMimeTypes.

        If the playback is stopped, starts playing
        If the uri scheme or the mime-type of the uri to open is not supported,
        this method does nothing and may raise an error.
        """

    def Seeked(postition):
        """Indicates that the track position has changed in a way
        that is inconsistant with the current playing state.
        Parameters
            position — The new position, in microseconds.

        This signal does not need to be emitted
        when playback starts or when the track changes,
        unless the track is starting at an unexpected position.
        """

    def PlaybackStatus(self):
        """The current playback status.
        May be "Playing", "Paused" or "Stopped".
        """

    def LoopStatus(self):
        """The current loop / repeat status
        May be:
            "None" if the playback will stop
                   when there are no more tracks to play
            "Track" if the current track will start again from
                    the begining once it has finished playing
            "Playlist" if the playback loops through a list of tracks
        """

    def Rate(self):
        """The current playback rate."""

    def Shuffle(self):
        """A value of false indicates that playback
        is progressing linearly through a playlist, while true means playback
        is progressing through a playlist in some other order.
        """

    def Metadata(self):
        """The metadata of the current element."""

    def Volume(self):
        """The volume level"""

    def Position(self):
        """The current track position in microseconds,
        between 0 and the 'mpris:length' metadata entry (see Metadata).
        """

    def MinimumRate(self):
        """The minimum value which the Rate property can take.
        This value should always be 1.0 or less.
        """

    def MaximumRate(self):
        """The maximum value which the Rate property can take.
        This value should always be 1.0 or greater."""

    def CanGoNext(self):
        """Whether the client can call the Next method on this interface
        and expect the current track to change.
        """

    def CanGoPrevious(self):
        """Whether the client can call the Previous method on this interface
        and expect the current track to change.
        """

    def CanPlay(self):
        """Whether playback can be started using Play or PlayPause."""

    def CanPause(self):
        """Whether playback can be paused using Pause or PlayPause."""

    def CanSeek(self):
        """Whether the client can control the playback position
        using Seek and SetPosition. This may be different for different tracks.
        """

    def CanControl(self):
        """Whether the media player may be controlled over this interface."""
