[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/wistful/pympris/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

# pympris #
This is a Python wrapper around the MPRIS2 interfaces of media players.

## Requires ##

[dbus-python>=1.0](http://dbus.freedesktop.org/releases/dbus-python/).

**pympris** depends on *dbus-python*, but *dbus-python* can't be installed automaticaly. That's why *dbus-python* wasn't included as a requirement.

## License ##
See the `LICENSE` file.

## Installation ##

pympris on pypi at http://pypi.python.org/pypi/pympris/

```python
pip install pympris
```
or
```python
easy_install pympris
```

## Usage ##

Setting up an event loop.
Needed only for receiving signals.
```python
from __future__ import print_function
from gi.repository import GObject
import dbus
from dbus.mainloop.glib import DBusGMainLoop
dbus_loop = DBusGMainLoop()
bus = dbus.SessionBus(mainloop=dbus_loop)
```

Import library and search available players
```python
import pympris

# get unique ids for all available players
players_ids = list(pympris.available_players())
```

Setup MediaPlayer object and print player Identity
```python
mp = pympris.MediaPlayer(players_ids[1], bus)

# mp.root implements org.mpris.MediaPlayer2 interface
# mp.player implements org.mpris.MediaPlayer2.Player
# mp.track_list implements org.mpris.MediaPlayer2.TrackList
# mp.playlists implements org.mpris.MediaPlayer2.Playlists

print(mp.root.Identity)
```

Playing with org.mpris.MediaPlayer2 interface
```python
if mp.root.CanRaise:
    mp.root.Raise()
mp.root.Fullscreen = True
```

Playing with org.mpris.MediaPlayer2.Player
```python
if mp.player.CanPlay and mp.player.CanPause:
    mp.player.PlayPause()

mp.player.Volume = mp.player.Volume*2

if mp.player.CanGoNext:
    mp.player.Next()
```

Playing with org.mpris.MediaPlayer2.TrackList
```python
tracks = mp.track_list.Tracks
for track_id in tracks:
    print(track_id)

if len(tracks) > 1:
    mp.track_list.RemoveTrack(tracks[-1])
    mp.track_list.GoTo(tracks[0])
```

Playing with org.mpris.MediaPlayer2.Playlists interface
```python
n = mp.playlists.PlaylistCount
ordering = pympris.PlaylistOrdering.LastPlayDate
playlists = mp.playlists.GetPlaylists(0, n, ordering, reversed=False)
pl_id, pl_name, pl_icon = playlists[-2]
mp.playlists.ActivatePlaylist(pl_id)
```

Setting up signal handlers
```python
def seeked(x):
    print(x)


def PlaylistChanged(arg):
    print("PlaylistChanged", arg)


def TrackMetadataChanged(track_id, metadata):
    print("TrackMetadataChanged", track_id, metadata)


def TrackListReplaced(tracks, current_track):
    print("TrackListReplaced", tracks, current_track)


def TrackAdded(metadata, after_track):
    print("TrackAdded", metadata, after_track)


def TrackRemoved(track_id):
    print("TrackRemoved", track_id)


mp.player.register_signal_handler('Seeked', seeked)
mp.playlists.register_signal_handler('PlaylistChanged', PlaylistChanged)
mp.track_list.register_signal_handler('TrackMetadataChanged',
                                      TrackMetadataChanged)
mp.track_list.register_signal_handler('TrackListReplaced', TrackListReplaced)
mp.track_list.register_signal_handler('TrackAdded', TrackAdded)
mp.track_list.register_signal_handler('TrackRemoved', TrackRemoved)


loop = GObject.MainLoop()
loop.run()
```
