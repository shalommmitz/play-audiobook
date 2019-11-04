import dbus, os, time

def toLog(msg):
    print msg

class AudioPlayer(object):
    def __init__(self):
        self.vlc = VLC()
        self.current_audio_file = None

    def is_new_book(self):
        return True

    def set_to_first_audio_file(self):
        self.current_audio_file = "test.mp3"
        
    def add_audio_file(self, file_name): 
        return self.vlc.add_audio_file(os.getcwd() +"/book/"+ file_name)
    def play(self): return self.vlc.play()
    def pause(self): return self.vlc.pause()
    def get_status(self): return self.vlc.get_status()
    def get_position(self): return self.vlc.get_position()
    def get_lenght(self): return self.vlc.get_lenght()

class VLC(object):
    # Launchs and controls VLC, using the dbus interface
    def __init__(self):
        player_interface     = 'org.mpris.MediaPlayer2.Player'
        tracklist_interface     = 'org.mpris.MediaPlayer2.TrackList'
        main_interface         = 'org.mpris.MediaPlayer2'

        self.pid = self.load()
        addr = "org.mpris.MediaPlayer2.vlc.instance"+ self.pid
        bus = dbus.SessionBus()
        vlc_obj = bus.get_object(addr, "/org/mpris/MediaPlayer2")
        self.main       = dbus.Interface(vlc_obj, dbus_interface=main_interface)
        self.player     = dbus.Interface(vlc_obj, dbus_interface=player_interface)
        self.tracklist  = dbus.Interface(vlc_obj, dbus_interface=tracklist_interface)
        self.prop       = dbus.Interface(vlc_obj, 'org.freedesktop.DBus.Properties')
        return         

    def load(self):
        # Do we have a running VLC ?
        pid = self.get_vlc_pid()
        if not pid:
            toLog("Launching VLC")
            os.system("nohup vlc -I dummy --control dbus &")
            toLog("waiting 2 seconds")
            time.sleep(2)
        # If not, lets try to launch it
        pid = self.get_vlc_pid()
        if not pid:
            toLog("Failed launching VLC - Aborting")
            exit()
        return pid
        
    def get_vlc_pid(self):
        return os.popen("pgrep vlc").read().strip()

    def play(self):
        self.player.Play()

    def pause(self):
        self.player.Pause()

    def get_status(self):
        return self.prop.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')

    def get_position(self):
        return self.prop.Get("org.mpris.MediaPlayer2.Player", "Position")
   
    def show_available_methods():
        props = self.prop.GetAll('org.mpris.MediaPlayer2')
        print "for root:"
        for k in props.keys():
            print "   ", k
        return
        print "for player:"
        props = self.prop.GetAll('org.mpris.MediaPlayer2.Player')
        for k in props.keys():
            print "   ", k
        return

    def get_metadata(self):
        return self.prop.Get("org.mpris.MediaPlayer2.Player", "Metadata")

    def get_lenght(self):
        # Return position, in micro seconds, of currently playing track
        return self.get_metadata()['mpris:length']

    def add_audio_file(self, fn):
        # Add audio file to playing list. 'fn' must be full path !
        obj_no_track = '/org/mpris/MediaPlayer2/TrackList/NoTrack'
        self.tracklist.AddTrack('file://' + fn, obj_no_track, True)


if __name__=="__main__":
    print "main"
    vlc = VLC()
    vlc.add_audio_file("/home/jon/play_audiobook/test.mp3")
    vlc.play()
    time.sleep(0.4)
    for i in range(1000):
        print "For time passed:", i*0.5
        print "    status:", vlc.get_status()
        print "    position:", vlc.get_position()
        print "    len:", vlc.get_lenght()
        time.sleep(0.5)
