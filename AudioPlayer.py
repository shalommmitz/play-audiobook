import dbus, os, time

def toLog(msg):
    print msg

class AudioPlayer(object):
    def __init__(self):
        self.vlc = VLC()
        self.current_audio_file = None


    def get_last_played_audio_file(self):
        def is_new_book(self):
            return True
        if is_new_book(self):
            file = "test.mp3"
        else:
            file = open("last_played_audio_file.txt").read().strip()
        toLog( "get_last_played_audio_file returned: "+ file)
        return file

    def set_audio_file(self, file_name): 
        self.vlc.clear_track_list()
        self.vlc.add_track(os.getcwd() +"/book/"+ file_name)
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
        toLog("Launched vlc, pid is "+ str(pid))
        return pid
        
    def get_vlc_pid(self):
        return os.popen("pgrep vlc").read().strip()

    def play(self):
        toLog("vlc: play")
        self.player.Play()

    def pause(self):
        toLog("vlc: pause")
        self.player.Pause()

    def get_status(self):
        status = self.prop.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus').strip()
        print "vlc: status is: "+ status
        return status

    def get_position(self):
        return self.prop.Get("org.mpris.MediaPlayer2.Player", "Position")
   
    def show_available_methods(self):
        def print_props(name, props):
            print "Properties of "+ name
            for k in props.keys():
                print "   ", k
            return
        props = self.prop.GetAll('org.mpris.MediaPlayer2')
        print_props("root", props)
        props = self.prop.GetAll('org.mpris.MediaPlayer2.Player')
        print_props("player", props)
        props = self.prop.GetAll('org.mpris.MediaPlayer2.TrackList')
        print_props("tracklist", props)
        return

    def get_metadata(self):
        return self.prop.Get("org.mpris.MediaPlayer2.Player", "Metadata")

    def get_num_tracks(self):
        tracks = self.prop.Get("org.mpris.MediaPlayer2.TrackList", "Tracks")
        num_tracks = len(tracks)
        return num_tracks

    def clear_track_list(self):
        def del_track():
            tracks = self.prop.Get("org.mpris.MediaPlayer2.TrackList", "Tracks")
            self.tracklist.RemoveTrack(tracks[0])
        num_tracks = self.get_num_tracks()
        while num_tracks:
            del_track()
            num_tracks = self.get_num_tracks()
        toLog("Cleared track list")

    def get_lenght(self):
        # Return position, in micro seconds, of currently playing track
        return self.get_metadata()['mpris:length']

    def add_track(self, fn):
        # Add audio file to playing list. 'fn' must be full path !
        obj_no_track = '/org/mpris/MediaPlayer2/TrackList/NoTrack'
        self.tracklist.AddTrack('file://' + fn, obj_no_track, True)
        self.pause()    #we want explicit play
        toLog("vlc: added the file '"+ fn +"' to the track list.")


if __name__=="__main__":
    print "main"
    vlc = VLC()
    #vlc.show_available_methods()
    #exit()
    num_tracks = vlc.get_num_tracks()
    print "len of track list:", num_tracks
    vlc.add_track("/home/jon/play_audiobook/book/test.mp3")
    num_tracks = vlc.get_num_tracks()
    print "len of track list:", num_tracks
    vlc.clear_track_list()
    num_tracks = vlc.get_num_tracks()
    print "len of track list:", num_tracks
    exit()
    vlc.play()
    time.sleep(0.4)
    for i in range(10):
        print "For time passed:", i*0.5
        print "    status:", vlc.get_status()
        print "    position:", vlc.get_position()
        print "    len:", vlc.get_lenght()
        time.sleep(0.5)
