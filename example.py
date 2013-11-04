import gobject
import dbus
from dbus.mainloop.glib import DBusGMainLoop

import pympris

dbus_loop = DBusGMainLoop()
bus = dbus.SessionBus(mainloop=dbus_loop)

# get unique ids for all available players
players_ids = list(pympris.available_players())
mp = pympris.MediaPlayer(players_ids[1], bus)

# mp.root implements org.mpris.MediaPlayer2 interface
# mp.player implements org.mpris.MediaPlayer2.Player
# mp.track_list implements org.mpris.MediaPlayer2.TrackList
# mp.playlists implements org.mpris.MediaPlayer2.Playlists

print mp.root.Identity

if mp.root.CanRaise:
    mp.root.Raise()

if mp.player.CanPlay and mp.player.CanPause:
    mp.player.PlayPause()

mp.player.Volume = mp.player.Volume*2

if mp.player.CanGoNext:
    mp.player.Next()

tracks = mp.track_list.Tracks
for track_id in tracks:
    print track_id

if len(tracks) > 1:
    mp.track_list.RemoveTrack(tracks[-1])
    mp.track_list.GoTo(tracks[0])

n = mp.playlists.PlaylistCount
ordering = pympris.PlaylistOrdering.LastPlayDate
playlists = mp.playlists.GetPlaylists(0, n, ordering, reversed=False)
pl_id, pl_name, pl_icon = playlists[-2]
mp.playlists.ActivatePlaylist(pl_id)

# setup signal handlers


def seeked(x):
    print(x)


def PlaylistChanged(arg):
    print "PlaylistChanged", arg


def TrackMetadataChanged(track_id, metadata):
    print "TrackMetadataChanged", track_id, metadata


def TrackListReplaced(tracks, current_track):
    print "TrackListReplaced", tracks, current_track


def TrackAdded(metadata, after_track):
    print "TrackAdded", metadata, after_track


def TrackRemoved(track_id):
    print "TrackRemoved", track_id


mp.player.register_signal_handler('Seeked', seeked)
mp.playlists.register_signal_handler('PlaylistChanged', PlaylistChanged)
mp.track_list.register_signal_handler('TrackMetadataChanged',
                                      TrackMetadataChanged)
mp.track_list.register_signal_handler('TrackListReplaced', TrackListReplaced)
mp.track_list.register_signal_handler('TrackAdded', TrackAdded)
mp.track_list.register_signal_handler('TrackRemoved', TrackRemoved)

loop = gobject.MainLoop()
loop.run()
