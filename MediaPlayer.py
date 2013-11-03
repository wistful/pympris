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
        self.player = Player
        self.playlists = PlayLists
        self.tack_list = TrackList


def main():
    mp = MediaPlayer(':1.8608')
    root = mp.root
    print(root.Identity)
    print(root.SupportedMimeTypes)


if __name__ == '__main__':
    main()
