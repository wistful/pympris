#!/usr/bin/env python
# coding=utf-8

# Copyright (c) Mikhail Mamrouski.
# See LICENSE for details.

"""
Module provides a `Root` class wich implements MPRIS2 Root interface:
http://specifications.freedesktop.org/mpris-spec/latest/Media_Player.html

Usage::

    from pympris import Root

    root = Root('org.mpris.MediaPlayer2.vlc')
    print(root.Identity)  # VLC media player

    if root.CanRaise:
        root.Raise()

    print("Supported Mime Types", root.SupportedMimeTypes)
    print("Supported Uri Schemes", root.SupportedUriSchemes)

    if root.CanQuit:
        root.Quit()
"""

from .Base import Base

__all__ = ('Root', )


class Root(Base):

    """Class implements methods and properties
    to work with MPRIS2 MediaPlayer2 interface.
    """

    IFACE = "org.mpris.MediaPlayer2"
    """The D-Bus MediaPlayer2 interface name"""

    def Raise(self):
        """Brings the media player's user interface to the front
        using any appropriate mechanism available.
        The media player may be unable to control how its user interface
        is displayed, or it may not have a graphical user interface at all.
        In this case, the CanRaise property is false
        and this method does nothing."""
        self.iface.Raise()

    def Quit(self):
        """Causes the media player to stop running.
        The media player may refuse to allow clients to shut it down.
        In this case, the CanQuit property is false
        and this method does nothing.
        Note: Media players which can be D-Bus activated,
        or for which there is no sensibly easy way to terminate
        a running instance (via the main interface or a notification area icon
        for example) should allow clients to use this method.
        Otherwise, it should not be needed.
        If the media player does not have a UI, this should be implemented."""
        self.iface.Quit()

    @property
    def CanQuit(self):
        """If false, calling Quit will have no effect,
        and may raise a NotSupported error.
        If true, calling Quit will cause the media application to attempt
        to quit (although it may still be prevented from quitting by the user,
        for example)."""
        return self.get('CanQuit')

    @property
    def Fullscreen(self):
        """This property is optional.
        Clients should handle its absence gracefully.
        Whether the media player is occupying the fullscreen.
        This is typically used for videos. A value of true indicates that
        the media player is taking up the full screen.
        Media centre software may well have this value fixed to true
        If CanSetFullscreen is true, clients may set this property to true
        to tell the media player to enter fullscreen mode,
        or to false to return to windowed mode.
        If CanSetFullscreen is false, then attempting to set this property
        should have no effect, and may raise an error.
        However, even if it is true, the media player may still be unable
        to fulfil the request, in which case attempting to set this property
        will have no effect (but should not raise an error)."""
        return self.get('Fullscreen')

    @Fullscreen.setter
    def Fullscreen(self, state):
        """Set Fullscreen property"""
        self.set('Fullscreen', state)

    @property
    def CanSetFullscreen(self):
        """If false, attempting to set Fullscreen will have no effect,
        and may raise an error.
        If true, attempting to set Fullscreen will not raise an error,
        and (if it is different from the current value) will cause
        the media player to attempt to enter or exit fullscreen mode.
        Note that the media player may be unable to fulfil the request.
        In this case, the value will not change.
        If the media player knows in advance that it will not be able
        to fulfil the request, however, this property should be false."""
        return self.get('CanSetFullscreen')

    @property
    def CanRaise(self):
        """If false, calling Raise will have no effect,
        and may raise a NotSupported error.
        If true, calling Raise will cause the media application to attempt
        to bring its user interface to the front,
        although it may be prevented from doing so
        (by the window manager, for example). """
        return self.get('CanRaise')

    @property
    def HasTrackList(self):
        """Indicates whether the /org/mpris/MediaPlayer2 object
        implements the org.mpris.MediaPlayer2.TrackList interface."""
        return self.get('HasTrackList')

    @property
    def Identity(self):
        """A friendly name to identify the media player to users.
        This should usually match the name found in .desktop files
        (eg: "VLC media player")."""
        return self.get('Identity')

    @property
    def DesktopEntry(self):
        """The basename of an installed .desktop file which complies
        with the Desktop entry specification,
        with the ".desktop" extension stripped.

        Example:
        The desktop entry file is "/usr/share/applications/vlc.desktop",
        and this property contains "vlc"
        """
        return self.get('DesktopEntry')

    @property
    def SupportedUriSchemes(self):
        """The URI schemes supported by the media player.
        This can be viewed as protocols supported by the player
        in almost all cases. Almost every media player will include support
        for the "file" scheme. Other common schemes are "http" and "rtsp".
        Note that URI schemes should be lower-case.
        """
        return self.get('SupportedUriSchemes')

    @property
    def SupportedMimeTypes(self):
        """The mime-types supported by the media player.
        Mime-types should be in the standard format
        (eg: audio/mpeg or application/ogg).
        """
        return self.get('SupportedMimeTypes')
