#!/usr/bin/env python
# coding=utf-8

# Copyright (c) Mikhail Mamrouski.
# See LICENSE for details.

"""
This module provides a `Player` class
wich implemented MPRIS2 Player interface:
http://specifications.freedesktop.org/mpris-spec/latest/Player_Interface.html

Usage:

player = Player('org.mpris.MediaPlayer2.vlc')
if player.CanPause:
    player.PlayPause()

player.Volume = player.Volume*2
player.Play()
if player.CanGoNext:
    player.Next()

if player.CanSeek:
    player.Seek = 15000000

"""

from common import converter, convert2dbus
from Base import Base


class Player(Base):

    """class implements methods and properties
    to working with MPRIS2 Player interface
    """

    IFACE = "org.mpris.MediaPlayer2.Player"

    def __init__(self, name, bus=None):
        super(Player, self).__init__(name, bus)

    def Next(self):
        """Skips to the next track in the tracklist."""
        self.iface.Next()

    def Previous(self):
        """Skips to the previous track in the tracklist."""
        self.iface.Previous()

    def Pause(self):
        """Pauses playback."""
        self.iface.Pause()

    def PlayPause(self):
        """Pauses playback."""
        self.iface.PlayPause()

    def Stop(self):
        """Stops playback."""
        self.iface.Stop()

    def Play(self):
        """Starts or resumes playback."""
        self.iface.Play()

    def Seek(self, offset):
        """Seeks forward in the current track
        Parameters
            Offset — The number of microseconds to seek forward.
        A negative value seeks back.
        """
        self.iface.Seek(convert2dbus(offset, 'x'))

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
        self.iface.SetPosition(convert2dbus(track_id, 'o'),
                               convert2dbus(position, 'x'))

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
        self.iface.OpenUri(uri)

    @property
    @converter
    def PlaybackStatus(self):
        """The current playback status.
        May be "Playing", "Paused" or "Stopped".
        """
        return self.get('PlaybackStatus')

    @property
    @converter
    def LoopStatus(self):
        """The current loop / repeat status
        May be:
            "None" if the playback will stop
                   when there are no more tracks to play
            "Track" if the current track will start again from
                    the begining once it has finished playing
            "Playlist" if the playback loops through a list of tracks
        """
        return self.get('LoopStatus')

    @LoopStatus.setter
    def LoopStatus(self, status):
        """The current loop / repeat status
        May be:
            "None" if the playback will stop
                   when there are no more tracks to play
            "Track" if the current track will start again from
                    the begining once it has finished playing
            "Playlist" if the playback loops through a list of tracks
        """
        self.set('LoopStatus', status)

    @property
    @converter
    def Rate(self):
        """The current playback rate."""
        return self.get('Rate')

    @Rate.setter
    def Rate(self, value):
        """The current playback rate."""
        self.set('Rate', value)

    @property
    @converter
    def Shuffle(self):
        """A value of false indicates that playback
        is progressing linearly through a playlist, while true means playback
        is progressing through a playlist in some other order.
        """
        return self.get('Shuffle')

    @Shuffle.setter
    def Shuffle(self, value):
        """A value of false indicates that playback
        is progressing linearly through a playlist, while true means playback
        is progressing through a playlist in some other order.
        """
        self.set('Shuffle', value)

    @property
    @converter
    def Metadata(self):
        """The metadata of the current element."""
        return self.get('Metadata')

    @property
    @converter
    def Volume(self):
        """The volume level"""
        return self.get('Volume')

    @Volume.setter
    def Volume(self, value):
        """The volume level"""
        self.set('Volume', value)

    @property
    @converter
    def Position(self):
        """The current track position in microseconds,
        between 0 and the 'mpris:length' metadata entry (see Metadata).
        """
        return self.get('Position')

    @property
    @converter
    def MinimumRate(self):
        """The minimum value which the Rate property can take.
        This value should always be 1.0 or less.
        """
        return self.get('MinimumRate')

    @property
    def MaximumRate(self):
        """The maximum value which the Rate property can take.
        This value should always be 1.0 or greater."""
        return self.get('MaximumRate')

    @property
    @converter
    def CanGoNext(self):
        """Whether the client can call the Next method on this interface
        and expect the current track to change.
        """
        return self.get('CanGoNext')

    @property
    @converter
    def CanGoPrevious(self):
        """Whether the client can call the Previous method on this interface
        and expect the current track to change.
        """
        return self.get('CanGoPrevious')

    @property
    @converter
    def CanPlay(self):
        """Whether playback can be started using Play or PlayPause."""
        return self.get('CanPlay')

    @property
    @converter
    def CanPause(self):
        """Whether playback can be paused using Pause or PlayPause."""
        return self.get('CanPause')

    @property
    @converter
    def CanSeek(self):
        """Whether the client can control the playback position
        using Seek and SetPosition. This may be different for different tracks.
        """
        return self.get('CanSeek')

    @property
    @converter
    def CanControl(self):
        """Whether the media player may be controlled over this interface."""
        return self.get('CanControl')
